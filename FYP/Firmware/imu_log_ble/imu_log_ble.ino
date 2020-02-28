#include <Arduino_LSM9DS1.h>
#include <ArduinoBLE.h>

#define IO_USERNAME "BohemianXen"
#define IO_KEY "aio_Mbeo57A4D24lfhO07ODfzvIOgKQy"

#//GLOBALS
const byte saveLED = 3;
const byte sendLED = 4;
const byte saveButton = 5; 
const byte sendButton = 6;
//const unsigned long debounceTime = 1000;
unsigned short totalSamples = 238; //sampleRates[0] * captureTimeSecs;
byte saveStatus, sendStatus = 0;
byte sampleRates [3] = {0, 0, 0}; // {IMU.accelerationSampleRate(), IMU.gyroscopeSampleRate(), IMU.magneticFieldSampleRate()};

//BLE
BLEService dataReadyService("a34984b9-7b89-4553-aced-242a0b289bbc");
BLEBoolCharacteristic dataReadyChar("4174c433-4064-4349-bfa2-009a432a24a4", BLERead | BLENotify);

BLEService imuService("f9dd156e-f108-4139-925c-dd1f157cffa0");
BLECharacteristic imuChar("41277a1b-b4f8-4ddc-871a-db0dd23a3a31", BLERead | BLENotify, 36);

BLEService sendDataService("ab36b3d9-12e4-4922-ac94-8873e8252045");
BLEBoolCharacteristic sendDataChar("976aca21-135a-4dfa-b548-68308f7acceb", BLERead | BLEWrite);

//BLEDevice central;


void setup() {
  // put your setup code here, to run once:
  pinMode(saveLED, OUTPUT);
  pinMode(sendLED, OUTPUT);
  pinMode(saveButton, INPUT);
  pinMode(sendButton, INPUT);
  
  Serial.begin(115200);
  
  if (!IMU.begin()) {
    Serial.println("Failed to initialise IMU!");
    while (1);
  } else {
    sampleRates[0] = IMU.accelerationSampleRate();
    sampleRates[1] = IMU.gyroscopeSampleRate(); 
    sampleRates[2] = IMU.magneticFieldSampleRate();

    /*Serial.print(sampleRates[0]);
    Serial.print(" Hz, ");
    Serial.print(sampleRates[1]);
    Serial.print(" Hz, ");
    Serial.print(sampleRates[2]);
    Serial.print(" Hz, ");
    Serial.println();*/
  }


  if (!BLE.begin()) {
    Serial.println("Failed to initialise BT Module!");
    while(1);
  }
  
  BLE.setLocalName("FallDetector");
  BLE.setDeviceName("FallDetector");

  dataReadyService.addCharacteristic(dataReadyChar);
  imuService.addCharacteristic(imuChar);
  sendDataService.addCharacteristic(sendDataChar);
  BLE.addService(dataReadyService);
  BLE.addService(imuService);
  BLE.addService(sendDataService);

  //sendDataChar.setEventHandler(BLEWritten, sendData);
   
  BLE.setAdvertisedService(dataReadyService);
  BLE.advertise();
  Serial.println("Advertising...");
}

void loop() {
  long imuDataL [totalSamples][9];
  bool dataReady = 0;
  BLEDevice central = BLE.central();
  
  if (central) {
    Serial.print("Connected to: ");
    Serial.println(central.address());
    digitalWrite(LED_BUILTIN, HIGH);
    dataReadyChar.writeValue(0);
    sendDataChar.writeValue(0);  
  
    while (central.connected()) {
        digitalWrite(sendLED, LOW);
        digitalWrite(saveLED, LOW);
        
        byte external_start = 0;
        sendDataChar.readValue(external_start);
        if (external_start) { Serial.println("Received start command from central"); }

        if (external_start || digitalRead(saveButton)) {
          Serial.println("Starting save in 3 seconds");
          blinkSaveLED(500); 
          dataReady = startSave(imuDataL);
          dataReadyChar.writeValue(dataReady);
          digitalWrite(saveLED, LOW);
          Serial.println("Saved!");
          //delay(100);
          bool dataSent = sendData(imuDataL);
          dataReadyChar.writeValue(0);
          sendDataChar.writeValue(0);
          digitalWrite(sendLED, LOW);
        }
    }
  }
  
  digitalWrite(LED_BUILTIN, LOW);
  Serial.print("Disconnected from: ");
  Serial.println(central.address());
  delay(200);
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

bool startSave(long imuDataL[][9]) {
  const bool readMag = false;
  const byte captureTimeSecs = 2;
  unsigned short samplesRead = 0;
  float imuDataF [totalSamples][9];
  bool success = 0;

  samplesRead = getVals(imuDataF, samplesRead, readMag);
  
  if (samplesRead == totalSamples) {
    digitalWrite(saveLED, LOW);
    digitalWrite(sendLED, HIGH);
    
    success = saveData(imuDataF, imuDataL);
    
    if (success) {
      Serial.println("Data save successful");
      //blinkSaveLED(20);  
    } else {
      Serial.println("Data save unsuccessful");
      digitalWrite(saveLED, LOW);
    } 
  }

  return success;
}


// TODO: add timeout based on millis
unsigned short getVals(float dataOut[][9], unsigned short sampleNo, bool readMag) {
  //bool ready = true;
  //float dataOut[9] = {0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0};
  int maxSamplePeriod = 1000/sampleRates[0];

  while (sampleNo != totalSamples && IMU.accelerationAvailable() && IMU.gyroscopeAvailable()) { 
      IMU.readAcceleration(dataOut[sampleNo][0], dataOut[sampleNo][1], dataOut[sampleNo][2]);
      IMU.readGyroscope(dataOut[sampleNo][3], dataOut[sampleNo][4], dataOut[sampleNo][5]);
      IMU.readMagneticField(dataOut[sampleNo][6], dataOut[sampleNo][7], dataOut[sampleNo][8]);
      sampleNo++; //Serial.println(sampleNo);
      delay(maxSamplePeriod);
      //if readMag 
      //if (sampleNo == totalSamples) { return sampleNo; }  
  }
  return sampleNo;
}  

bool saveData(float imuDataF[][9], long imuDataL[][9]) {
   Serial.println("Sending data...");
   int totalRead = 0;
   for (int i = 0; i < totalSamples; i++) {
    for (int j = 0; j < 9; j++) {
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
   Serial.println(totalRead);
   if (totalRead == (totalSamples*9)) {
    return 1;  
   } else {
    return 0;
   }
} 

bool sendData(long imuDataL[][9]) {
  int totalSent = 0;

   for (int i = 0; i < totalSamples; i++) {
     byte buff[36];
     byte offset = 0;
         
    for (int j = 0; j < 9; j++) {
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
    }
    
    imuChar.writeValue(buff, 36);
   }

   if (totalSent== (totalSamples*9)) {
    return 1;  
   } else {
    return 0;
   }
}
