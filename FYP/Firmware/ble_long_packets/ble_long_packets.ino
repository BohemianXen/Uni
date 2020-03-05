#include <Arduino_LSM9DS1.h>
#include <ArduinoBLE.h>

#define IO_USERNAME "BohemianXen"
#define IO_KEY "aio_Mbeo57A4D24lfhO07ODfzvIOgKQy"

#//GLOBALS
const byte saveLED = 3;
const byte sendLED = 4;
const byte saveButton = 5; 
const byte sendButton = 6;

const byte sampleLength = 6; //No. of parameters in a single sample (9 if all, 6 w/o magnetometer)
const byte packetLength = 10; // No. of samples in a single data packet
const unsigned short packetSize = sampleLength * packetLength * 4; // No. of bytes in an entire packet
//const unsigned long debounceTime = 1000;
unsigned short totalSamples = 480; //sampleRates[0] * captureTimeSecs;
unsigned short totalPackets = totalSamples/packetLength; //TODO: What do to if float result
byte saveStatus, sendStatus = 0;
byte sampleRates [3] = {0, 0, 0}; // {IMU.accelerationSampleRate(), IMU.gyroscopeSampleRate(), IMU.magneticFieldSampleRate()};

//BLE
BLEService dataReadyService("a34984b9-7b89-4553-aced-242a0b289bbc");
BLEBoolCharacteristic dataReadyChar("4174c433-4064-4349-bfa2-009a432a24a4", BLERead | BLENotify);

BLEService imuService("f9dd156e-f108-4139-925c-dd1f157cffa0");
BLECharacteristic imuChar("41277a1b-b4f8-4ddc-871a-db0dd23a3a31", BLERead | BLEIndicate, packetSize);

BLEService sendDataService("ab36b3d9-12e4-4922-ac94-8873e8252045");
BLEBoolCharacteristic sendDataChar("976aca21-135a-4dfa-b548-68308f7acceb", BLERead | BLEWrite);

BLEService startingStreamService("05b7f95e-0d89-43da-973c-3aa5a67b6031");
BLEBoolCharacteristic startingStreamChar("20b35680-9cf5-4f41-bde9-308abbc3c019", BLERead | BLENotify);

//BLEDevice central;


void setup() {
  // put your setup code here, to run once:
  pinMode(saveLED, OUTPUT);
  pinMode(sendLED, OUTPUT);
  pinMode(saveButton, INPUT);
  pinMode(sendButton, INPUT);
  //pinMode(7, INPUT);
  
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

  //sendDataChar.setEventHandler(BLEWritten, sendData);
   
  BLE.setAdvertisedService(dataReadyService);
  BLE.advertise();
}

void loop() {
  long imuDataL [totalSamples][sampleLength];
  initialiseData(imuDataL);
  bool dataReady = 0;
  BLEDevice central = BLE.central();
  
  if (central) {
    Serial.print("Connected to: ");
    Serial.println(central.address());
    digitalWrite(LED_BUILTIN, HIGH);
    dataReadyChar.writeValue(0);
    sendDataChar.writeValue(0);
    startingStreamChar.writeValue(0);  
  
    while (central.connected()) {
        digitalWrite(sendLED, LOW);
        digitalWrite(saveLED, LOW);
        
        byte external_start = 0;
        sendDataChar.readValue(external_start);
        bool startStream = external_start || digitalRead(saveButton);

        if (startStream) {
          startingStreamChar.writeValue(1);
          blinkSaveLED(500); 
          dataReady = startSave(imuDataL);
          dataReadyChar.writeValue(dataReady);
          digitalWrite(saveLED, LOW);
          //delay(100);
          bool dataSent = sendData(imuDataL);
          dataReadyChar.writeValue(0);
          sendDataChar.writeValue(0);
          startingStreamChar.writeValue(0);
          digitalWrite(sendLED, LOW);
        }
    }
  }
  
  digitalWrite(LED_BUILTIN, LOW);
  Serial.print("Disconnected from: ");
  Serial.println(central.address());
  delay(200);
}

void initialiseData(long imuDataL[][sampleLength]) {
  for (int i = 0; i < totalSamples; i++) {
    for (int j = 0; j < sampleLength; j++) {
      imuDataL[i][j] = 0;
    }
  }
}


void blinkSaveLED(int period) {
  digitalWrite(saveLED, HIGH);
  delay(period);
  digitalWrite(saveLED, LOW); 
  delay(period); 
  digitalWrite(saveLED,HIGH);
  delay(period);
  digitalWrite(saveLED, LOW);
  delay(period);
  digitalWrite(saveLED, HIGH); 
  delay(period); 
  digitalWrite(saveLED,LOW);
  delay(period);
  if (period == 500) { digitalWrite(saveLED, HIGH); }
}

bool startSave(long imuDataL[][sampleLength]) {
  const bool readMag = (sampleLength == 9);
  const byte captureTimeSecs = 2;
  unsigned short samplesRead = 0;
  float imuDataF [totalSamples][sampleLength];
  bool success = 0;
  
  initialiseData(imuDataL);
  samplesRead = getVals(imuDataF, samplesRead, readMag);
  
  if (samplesRead == totalSamples) {
    digitalWrite(saveLED, LOW);
    digitalWrite(sendLED, HIGH);
    
    success = saveData(imuDataF, imuDataL);
    
    if (!success) { blinkSaveLED(50); }
  }

  return success;
}


// TODO: add timeout based on millis
unsigned short getVals(float dataOut[][sampleLength], unsigned short sampleNo, bool readMag) {
  int minSamplePeriod = 1000/sampleRates[0];

  while (sampleNo != totalSamples && IMU.accelerationAvailable() && IMU.gyroscopeAvailable()) {
      IMU.readAcceleration(dataOut[sampleNo][0], dataOut[sampleNo][1], dataOut[sampleNo][2]);
      IMU.readGyroscope(dataOut[sampleNo][3], dataOut[sampleNo][4], dataOut[sampleNo][5]);

      /*if (readMag) {
        Serial.println(IMU.magneticFieldAvailable());
        IMU.readMagneticField(dataOut[sampleNo][6], dataOut[sampleNo][7], dataOut[sampleNo][8]);
      }*/
      
      sampleNo++;
      //Serial.println(sampleNo);
      delay(minSamplePeriod);  
  }
  Serial.println("Done");
  return sampleNo;
}  

bool saveData(float imuDataF[][sampleLength], long imuDataL[][sampleLength]) {
   Serial.println("Sending data...");
   int totalRead = 0;
   for (int i = 0; i < totalSamples; i++) {
    for (int j = 0; j < sampleLength; j++) {
      float scaled = imuDataF[i][j] * 1000.0;
      imuDataL[i][j] = (long) scaled;
      //imuChar.writeValue(imuDataL[i][j]);
      totalRead++; 
      Serial.print(imuDataL[i][j]);
      Serial.print(",");
    }
    Serial.println();
    //delay(10);
   }
   //Serial.println(totalRead);
   if (totalRead == (totalSamples*sampleLength)) {
    return 1;  
   } else {
    return 0;
   }
} 

bool sendData(long imuDataL[][sampleLength]) {
  int totalSent = 0;
  bool success = 1;
  //int start = 0;
  
   
   for (int packetStart = 0; packetStart < totalSamples; packetStart += packetLength) {
    byte buff[packetSize];
    unsigned short offset = 0;
     for (int i = packetStart; i < (packetStart + packetLength); i++) {
      //Serial.println(packetStart);
      for (int j = 0; j < sampleLength; j++) {
        byte shift = 0;
        //Serial.print("Pre-Shift:\t");
        //Serial.println(imuDataL[i][j], BIN); 
        for (int k = 0; k < 4; k++) {
          buff[k+offset] = (byte) (imuDataL[i][j] >> shift);
          shift += 8;
          //Serial.print("Post-Shift:\t");
          //Serial.println(buff[k+offset], BIN); 
        }     
        offset += 4;
        totalSent++;
        //Serial.println(offset);
        //Serial.println(totalSent);
      }
     }
      // ---------------- Attempt to send data packet --------------
     int retries = 3;
     success = imuChar.writeValue(buff, packetSize);
     delay(5);
    
    if(!success) {
       Serial.print("Failed to write sample: ");
       Serial.println(totalSent);
       //Serial.println("Re-trying");
      
      do {
        success = imuChar.writeValue(buff, packetSize);
        retries--;
        delay(100);
      } while (!success && (retries != 0)); 

      if (!success) {
        delay(3000);
        return 0; 
      }
    }
     
     //delay(100);
     //start += packetLength;
   }

   if (success && (totalSent == (totalSamples*sampleLength))) {
    return 1;  
   } else {
    return 0;
   }
}
