// TODO: Fix mixed indentations introduced by Arduino IDE

/* -------------------------------------------------- INCLUDES ------------------------------------------------*/

#include <Arduino_LSM9DS1.h>
#include <ArduinoBLE.h>

/* -------------------------------------------------- GLOBALS -------------------------------------------------*/

#define SAVE_LED 3
#define SEND_LED 4
#define RECORD_BUTTON 5
#define LIVE_MODE 0

#if LIVE_MODE
const unsigned short totalSamples = 40;
#else
const unsigned short totalSamples = 480;
#endif

const byte sampleLength = 6; // No. of parameters in a single sample (9 if all, 6 w/o magnetometer)
const byte packetLength = 8; // No. of samples in a single data packet
const unsigned short packetSize = sampleLength * packetLength * 4; // No. of bytes in an entire packet
const unsigned short totalPackets = totalSamples/packetLength; // TODO: Handle float result if developer is careless

byte saveStatus, sendStatus = 0;
byte sampleRates [3] = {0, 0, 0};

/* For debug only -- TODO: #define DEBUG and refactor code to reflect this
unsigned long timer1 = 0; 
unsigned long timer2 = 0; */

/* ----------------------------------------------------- BLE ---------------------------------------------------*/

BLEService dataReadyService("a34984b9-7b89-4553-aced-242a0b289bbc");
BLEBoolCharacteristic dataReadyChar("4174c433-4064-4349-bfa2-009a432a24a4", BLERead | BLENotify);

BLEService imuService("f9dd156e-f108-4139-925c-dd1f157cffa0");
BLECharacteristic imuChar("41277a1b-b4f8-4ddc-871a-db0dd23a3a31", BLERead | BLEIndicate, packetSize);

BLEService sendDataService("ab36b3d9-12e4-4922-ac94-8873e8252045");
BLEBoolCharacteristic sendDataChar("976aca21-135a-4dfa-b548-68308f7acceb", BLERead | BLEWrite);

BLEService startingStreamService("05b7f95e-0d89-43da-973c-3aa5a67b6031");
BLEBoolCharacteristic startingStreamChar("20b35680-9cf5-4f41-bde9-308abbc3c019", BLERead | BLENotify);

/* -------------------------------------------------- SETUP -------------------------------------------------*/

void setup() {
  pinMode(SAVE_LED, OUTPUT);
  pinMode(SEND_LED, OUTPUT);
  pinMode(RECORD_BUTTON, INPUT);
  
  Serial.begin(115200);
  
  if (!IMU.begin()) {
    Serial.println("Failed to initialise IMU");
    while (1);
  } else {
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
  BLE.setConnectionInterval(0x0006, 0x0028); // Ask central to poll more frequently given large payloads
  BLE.advertise();
}

/* ------------------------------------------------ MAIN LOOP -------------------------------------------------*/

void loop() {
  // Inits
  long imuDataL [totalSamples][sampleLength];
  initialiseData(imuDataL);
  bool dataReady = 0;
  byte external_start = 0;
  BLEDevice central = BLE.central();
  
  if (central) {
    Serial.print("Connected to: ");
    Serial.println(central.address());
    digitalWrite(LED_BUILTIN, HIGH);
    dataReadyChar.writeValue(0);
    sendDataChar.writeValue(0);
    startingStreamChar.writeValue(0);  
  
    while (central.connected()) {
        digitalWrite(SEND_LED, LOW);
        digitalWrite(SAVE_LED, LOW);
        
        sendDataChar.readValue(external_start); // Check if start initiated through app
        delay(100);
        bool startStream = external_start || digitalRead(RECORD_BUTTON);  // Read pushbutton too

        if (LIVE_MODE && startStream) {
            liveStream(central, imuDataL);
        } else if (startStream) {
          // Indicate that device is streaming using appropriate characteristic as well as 3s LED blink
          startingStreamChar.writeValue(1);  
          blinkLED(SAVE_LED, 500, HIGH); 

          dataReady = startSave(imuDataL);
          dataReadyChar.writeValue(dataReady); // Indicate if data is ready
          digitalWrite(SAVE_LED, LOW);

          if (dataReady) {
              bool dataSent = sendData(imuDataL);  // TODO: What to do if somehow returns false
              dataReadyChar.writeValue(0);
              sendDataChar.writeValue(0);
              startingStreamChar.writeValue(0);
              digitalWrite(SEND_LED, LOW);
              delay(100);
          }
        }
        else {
            delay(10);
        }
    }
  }
  
  digitalWrite(LED_BUILTIN, LOW);
  Serial.print("Disconnected from: ");
  Serial.println(central.address());
  delay(200);
}

/* ------------------------------------------------ LIVE LOOP -------------------------------------------------*/

void liveStream(BLEDevice central, long imuDataL[][sampleLength]) {
    bool stopStream, dataSent, dataReady = 0;
    startingStreamChar.writeValue(1);
    blinkLED(SAVE_LED, 500, HIGH);

    while (!stopStream && central.connected()) {
        dataSent = 0;
        dataReady = startSave(imuDataL);
        // dataReadyChar.writeValue(dataReady);
        if (dataReady) { dataSent = sendData(imuDataL); }

        if (!dataSent || digitalRead(RECORD_BUTTON)) {
            dataReadyChar.writeValue(0);
            sendDataChar.writeValue(0);
            startingStreamChar.writeValue(0);
            digitalWrite(SAVE_LED, LOW);
            break;
        }
        delay(10);
    }

    blinkLED(SEND_LED, 500, LOW);
}

/* ------------------------------------------------ SUBROUTINES -------------------------------------------------*/

void initialiseData(long imuDataL[][sampleLength]) {
  for (int i = 0; i < totalSamples; i++) {
    for (int j = 0; j < sampleLength; j++) {
      imuDataL[i][j] = 0;
    }
  }
}


void blinkLED(int LED, int period, int end) {
    int toggle = HIGH;
    for (int i = 0; i < 6; i++) {
        digitalWrite(LED, toggle);
        delay(period);
        toggle = !toggle;
    }
    digitalWrite(LED, end);
}



bool startSave(long imuDataL[][sampleLength]) {
  // Inits
  const bool readMag = (sampleLength == 9);
  const byte captureTimeSecs = 2;
  unsigned short samplesRead = 0;
  float imuDataF [totalSamples][sampleLength];
  bool success = 0;
  initialiseData(imuDataL);

  samplesRead = getVals(imuDataF, samplesRead, readMag);  // Read samples, total no. read will be returned here
  
  if (samplesRead == totalSamples) {
      if (!LIVE_MODE) {
          digitalWrite(SAVE_LED, LOW);
          digitalWrite(SEND_LED, HIGH);
      }
      
      success = saveData(imuDataF, imuDataL);  // Scale floats and copy to long
      if (!success) { blinkLED(SAVE_LED, 50, LOW); }
}

  return success;
}


unsigned short getVals(float dataOut[][sampleLength], unsigned short sampleNo, bool readMag) {
  int minSamplePeriod = 1000/sampleRates[0];  // TODO: add timeout based on millis

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
   } else {
     return 0;
   }
} 


bool sendData(long imuDataL[][sampleLength]) {
    // Inits
    int totalSent = 0;
    bool success = 1;
    
    // Iterate over each sample and pack into byte buffer - sends packet and loops when this is full 
    for (int packetStart = 0; packetStart < totalSamples; packetStart += packetLength) {
        byte buff[packetSize];
        unsigned short offset = 0;
        // timer1 = millis(); for debug
        
        for (int i = packetStart; i < (packetStart + packetLength); i++) {
            for (int j = 0; j < sampleLength; j++) {
                byte shift = 0;
                // Serial.print("Pre-Shift:\t");
                // Serial.println(imuDataL[i][j], BIN);
                
                for (int k = 0; k < 4; k++) {
                    buff[k+offset] = (byte) (imuDataL[i][j] >> shift);
                    shift += 8;
                    // Serial.print("Post-Shift:\t");
                    // Serial.println(buff[k+offset], BIN); 
                }     
                
                offset += 4;
                totalSent++;
            }
        }
        
        // Attempt to send data packet
        
        // timer2 = millis();
        int retries = 3;
        success = imuChar.writeValue(buff, packetSize);
        // Serial.println(timer2 - timer1);
        // Serial.println(timer2 - millis());
         delay(5);
         if(!success) {
             Serial.print("Failed to write sample: ");
             Serial.println(totalSent);
             delay(20);
             // Serial.println("Re-trying");
             
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
    } else {
        return 0;
    }
}
