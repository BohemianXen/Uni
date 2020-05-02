/**
* @file training.ino
*
* Firmware for the training device. 
* Allows for training data collection in standard and live mode (depending on build config LIVE_MODE).
*
* @author Ralph Mukusa
* contact: ralph.mukusa@gmail.com
*
* version: 1.0
**/


/*----------------------------------------------------- INCLUDES --------------------------------------------------*/

#include <Arduino_LSM9DS1.h>
#include <ArduinoBLE.h>

/*----------------------------------------------------- GLOBALS ---------------------------------------------------*/

#define LIVE_MODE 1  // Continuous vs. single shot recording and uploading - latter is also when off-board processing

#define SAVE_LED 3
#define SEND_LED 4
#define RECORD_BUTTON 5

#if LIVE_MODE
const unsigned short totalSamples = 40;  // Send 40 samples at a time when in live streaming mode
#else
const unsigned short totalSamples = 480;  // Equates to ~4 second recording (119Hz sample rate) for collecting training data
#endif

const byte sampleLength = 6;  // No. of values in a single sample (9 if all, 6 w/o magnetometer)
const byte packetLength = 8;  // No. of samples in a single data packet
const unsigned short packetSize = sampleLength * packetLength * 4;  // No. of bytes in an entire packet
const unsigned short totalPackets = totalSamples/packetLength;  // TODO: Handle float result if developer is careless

byte sampleRates [3] = {0, 0, 0};

/* ------------------------------------------------------- BLE -----------------------------------------------------*/

BLEService dataReadyService("a34984b9-7b89-4553-aced-242a0b289bbc");
BLEBoolCharacteristic dataReadyChar("4174c433-4064-4349-bfa2-009a432a24a4", BLERead | BLENotify);

BLEService imuService("f9dd156e-f108-4139-925c-dd1f157cffa0");
BLECharacteristic imuChar("41277a1b-b4f8-4ddc-871a-db0dd23a3a31", BLERead | BLEIndicate, packetSize);

BLEService sendDataService("ab36b3d9-12e4-4922-ac94-8873e8252045");
BLEBoolCharacteristic sendDataChar("976aca21-135a-4dfa-b548-68308f7acceb", BLERead | BLEWrite);

BLEService startingStreamService("05b7f95e-0d89-43da-973c-3aa5a67b6031");
BLEBoolCharacteristic startingStreamChar("20b35680-9cf5-4f41-bde9-308abbc3c019", BLERead | BLENotify);

/* ------------------------------------------------------ SETUP ----------------------------------------------------*/
/**
* Arduino setup function. Runs on initial boot and resets.
**/
void setup() {
    pinMode(SAVE_LED, OUTPUT);
    pinMode(SEND_LED, OUTPUT);
    pinMode(RECORD_BUTTON, INPUT);
    
    Serial.begin(115200);
    
    if (!IMU.begin()) {
        Serial.println("Failed to initialise IMU");
        while (1);
    } 
    else {
        sampleRates[0] = IMU.accelerationSampleRate();
        sampleRates[1] = IMU.gyroscopeSampleRate(); 
        sampleRates[2] = IMU.magneticFieldSampleRate();
    }
    
    if (!BLE.begin()) {
        Serial.println("Failed to initialise BT Module");
        while(1);
    }
    
    // Name device then add BLE Services and Characteristics
    BLE.setLocalName("FallDetector");
    BLE.setDeviceName("FallDetector");
    
    dataReadyService.addCharacteristic(dataReadyChar);
    imuService.addCharacteristic(imuChar);
    sendDataService.addCharacteristic(sendDataChar);
    startingStreamService.addCharacteristic(startingStreamChar);
    
    BLE.addService(dataReadyService);
    BLE.addService(imuService);
    BLE.addService(sendDataService);
    BLE.addService(startingStreamService);
    BLE.setAdvertisedService(dataReadyService);
    
    // Ask central to poll more frequently (1.25ms(6, 40)) given large payloads 
    BLE.setConnectionInterval(0x0006, 0x0028);     
    
    BLE.advertise();
}

/*----------------------------------------------------- MAIN LOOP --------------------------------------------------*/
/**
* Arduino main loop function.
**/
void loop() {
    // Inits
    long imuDataL [totalSamples][sampleLength];
    initialiseData(imuDataL);
    bool dataReady = 0;
    byte external_start = 0;  // Used for signalling a received start from the UI
    BLEDevice central = BLE.central();
    
    if (central) {
        Serial.print("Connected to: ");
        Serial.println(central.address());
        digitalWrite(LED_BUILTIN, HIGH);
        
        // Update characteristics
        dataReadyChar.writeValue(0);
        sendDataChar.writeValue(0);
        startingStreamChar.writeValue(0);  
        
        while (central.connected()) {
            digitalWrite(SEND_LED, LOW);
            digitalWrite(SAVE_LED, LOW);
            
            sendDataChar.readValue(external_start);  // Check if start initiated through app
            delay(100);
            bool startStream = external_start || digitalRead(RECORD_BUTTON);  // Read pushbutton too
            
            if (LIVE_MODE && startStream) {
                liveStream(central, imuDataL);
            } 
            else if (startStream) {
                // Indicate that device is recording using appropriate characteristic as well as 3s LED blink
                startingStreamChar.writeValue(1);  
                blinkLED(SAVE_LED, 500, HIGH); 
                dataReady = startSave(imuDataL);
                dataReadyChar.writeValue(dataReady); // Indicate if data is ready
                digitalWrite(SAVE_LED, LOW);
                
                if (dataReady) {
                    // Full packet recorded, send it to client
                    bool dataSent = sendData(imuDataL);  // TODO: What to do if somehow returns false
                    
                    // Post upload re-inits
                    dataReadyChar.writeValue(0);
                    sendDataChar.writeValue(0);
                    startingStreamChar.writeValue(0);
                    digitalWrite(SEND_LED, LOW);
                    delay(100);
                }
            }
            else {
                delay(10);  // Not recording or streaming so just keep looping
            }
        }
    }
    
    // Client has disconnected
    digitalWrite(LED_BUILTIN, LOW);
    Serial.print("Disconnected from: ");
    Serial.println(central.address());
    delay(200);
}

/* ---------------------------------------------------- LIVE LOOP --------------------------------------------------*/

/**
 * Loop for maintaining a live stream.
 *
 * @param BLEDevice central: The BLE client for this server.
 * @param long** imuDataL: 2D array holding the scaled IMU readings.
**/
void liveStream(BLEDevice central, long imuDataL[][sampleLength]) {
    bool stopStream, dataSent, dataReady = 0;
    startingStreamChar.writeValue(1);  // Tell client the stream is about to start
    blinkLED(SAVE_LED, 500, HIGH);

    while (!stopStream && central.connected()) {
        dataSent = 0;
        dataReady = startSave(imuDataL);
        
        // Send data if packet ready
        if (dataReady) { dataSent = sendData(imuDataL); }

        // If packet not ready or user toggles recording off using button, stop stream
        if (!dataSent || digitalRead(RECORD_BUTTON)) {
            dataReadyChar.writeValue(0);
            sendDataChar.writeValue(0);
            startingStreamChar.writeValue(0);
            digitalWrite(SAVE_LED, LOW);
            break;
        }
        delay(10);
    }

    blinkLED(SEND_LED, 500, LOW);  // Blink red LED to signal end of stream
}

/* -------------------------------------------------- SUBROUTINES --------------------------------------------------*/


/**
 * Initialises a 2D long type array with all zeros.
 *
 * @param long** imuDataL: 2D array holding the scaled IMU readings.
**/
void initialiseData(long imuDataL[][sampleLength]) {
    for (int i = 0; i < totalSamples; i++) {
        for (int j = 0; j < sampleLength; j++) {
            imuDataL[i][j] = 0;
        }
    }
}


/**
 * Blinks an LED 6 times at the requested frequency.
 *
 * @param int LED: The digital pin number of the LED to be toggled.
 * @param int period: The blinking interval.
 * @param int end: The desired end state of the LED, either HIGH or LOW.
**/
void blinkLED(int LED, int period, int end) {
    // TODO: Sanity check input values
    int toggle = HIGH;
    for (int i = 0; i < 6; i++) {
        digitalWrite(LED, toggle);
        delay(period);
        toggle = !toggle;
    }
    digitalWrite(LED, end);
}


/**
 * Records the desired amount of IMU samples.
 *
 * @param long** imuDataL: 2D array holding the scaled IMU readings.
 * @return bool: Whether or not all samples were successfully recorded. 
**/
bool startSave(long imuDataL[][sampleLength]) {
    // Inits
    const byte captureTimeSecs = 2;
    float imuDataF [totalSamples][sampleLength];  // IMU module saves as float
    bool success = 0;
    initialiseData(imuDataL);  // Initialise just in case this is being entered within connected loop
    
    unsigned short samplesRead = getVals(imuDataF);  // Read samples, total no. read will be returned here
    
    if (samplesRead == totalSamples) {
        if (!LIVE_MODE) {
            digitalWrite(SAVE_LED, LOW);
            digitalWrite(SEND_LED, HIGH);
        }
        
        success = saveData(imuDataF, imuDataL);  // Scale floats and copy to long array
        if (!success) { blinkLED(SAVE_LED, 50, LOW); }
    }
    return success;
}


/**
 * Reads the Acc and Gyro, storing the values in the passed array.
 *
 * @param float** dataOut: 2D float array where the IMU readings will be stored.
 * @return unsigned short: Number of samples successfully read.
**/
unsigned short getVals(float dataOut[][sampleLength]) {
    unsigned short sampleNo = 0;
    int minSamplePeriod = 1000/sampleRates[0];  // Cap read rate to ensure new samples will always be available
    
    while (sampleNo != totalSamples && IMU.accelerationAvailable() && IMU.gyroscopeAvailable()) {
        IMU.readAcceleration(dataOut[sampleNo][0], dataOut[sampleNo][1], dataOut[sampleNo][2]);
        IMU.readGyroscope(dataOut[sampleNo][3], dataOut[sampleNo][4], dataOut[sampleNo][5]);
        sampleNo++;
        // Serial.println(sampleNo);
        delay(minSamplePeriod);  
    }
    
    Serial.println("Done");
    return sampleNo;
}  


/**
 * Converts the float IMU readings into scaled longs and saves them in main data array.
 *
 * @param float** imuDataF: 2D float array holding the IMU readings as floats.
 * @param long** imuDataL: 2D float array holding the IMU readings as scaled longs.
 * @return bool: Whether or not all samples were successfully converted and copied.
**/
bool saveData(float imuDataF[][sampleLength], long imuDataL[][sampleLength]) {
    Serial.println("Saving data...");
    int totalRead = 0;
    
    for (int i = 0; i < totalSamples; i++) {
        for (int j = 0; j < sampleLength; j++) {
            float scaled = imuDataF[i][j] * 1000.0; // Scale floats
            imuDataL[i][j] = (long) scaled;
            totalRead++; 
            Serial.print(imuDataL[i][j]);
            Serial.print(",");
        }
        Serial.println();
        // delay(10); for debug
    }
    
    // Serial.println(totalRead); for debug
    if (totalRead == (totalSamples*sampleLength)) {
        return 1;  
    } 
    else {
        return 0;
    }
} 


/**
 * Uploads the IMU data via the imuChar characteristic one little endian packet at a time.
 *
 * @param long** imuDataL: 2D float array holding the IMU readings as scaled longs.
 * @return bool: Whether or not all samples were successfully uploaded.
**/
bool sendData(long imuDataL[][sampleLength]) {
    // Inits
    int totalSent = 0;
    bool success = 1;
    
    // Iterate over each acc/gyro value and pack into byte buffer - sends packet and loops when this is full 
    for (int packetStart = 0; packetStart < totalSamples; packetStart += packetLength) {
        byte buff[packetSize];
        unsigned short offset = 0;
        
        for (int i = packetStart; i < (packetStart + packetLength); i++) {
            for (int j = 0; j < sampleLength; j++) {
                // For each individual acc/gyro value... 
                byte shift = 0;
                
                // Pack the long value (of size 4 bytes) into buffer one byte at a time, little endian style.
                for (int k = 0; k < 4; k++) {
                    buff[k+offset] = (byte) (imuDataL[i][j] >> shift);  // Shift sought byte to lowest 8 bits and copy to buffer 
                    shift += 8;
                }     
                
                offset += 4;  // Ready for next 4 bytes that represent the next long
                totalSent++;
            }
        }
        
        // Attempt to send data packet and wait for indication of success from client
        int retries = 3;
        success = imuChar.writeValue(buff, packetSize);
        delay(5);
        
        // Re-try thrice if failed to write packet
        if(!success) {
            Serial.print("Failed to write sample: ");
            Serial.println(totalSent);
            delay(20);
            Serial.println("Re-trying");
            
            do {
                success = imuChar.writeValue(buff, packetSize);
                retries--;
                delay(50);
            } while (!success && (retries != 0)); 
             
            if (!success) { return 0; }
        }
    }
    
    if (success && (totalSent == (totalSamples*sampleLength))) {
        return 1;  
    } 
    else {
        return 0;
    }
}
