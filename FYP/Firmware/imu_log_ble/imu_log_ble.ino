#include <Arduino_LSM9DS1.h>
#include <ArduinoBLE.h>

#define IO_USERNAME "BohemianXen"
#define IO_KEY "aio_Mbeo57A4D24lfhO07ODfzvIOgKQy"

#//GLOBALS
const byte saveLED = 3;
const byte sendLED = 4;
const byte saveButton = 5; 
const byte sendButton = 6;
unsigned long debounceTime = 1000;
//unsigned long 
byte saveStatus, sendStatus = 0;
byte sampleRates [3] = {0, 0, 0}; // {IMU.accelerationSampleRate(), IMU.gyroscopeSampleRate(), IMU.magneticFieldSampleRate()};

//BLE
BLEService accXService("1001");
BLEService accYService("1002");
BLEService accZService("1003");
BLEService gyroXService("0101");
BLEService gyroYService("0102");
BLEService gyroZService("0103");
BLEService magXService("0011");
BLEService magYService("0012");
BLEService magZService("0013");

BLELongCharacteristic accXChar("2001", BLERead | BLENotify); //| BLEIndicate);
BLELongCharacteristic accYChar("2002", BLERead | BLENotify); //| BLEIndicate);
BLELongCharacteristic accZChar("2003", BLERead | BLENotify); //| BLEIndicate);
BLELongCharacteristic gyroXChar("0201", BLERead | BLENotify); //| BLEIndicate);
BLELongCharacteristic gyroYChar("0202", BLERead | BLENotify); //| BLEIndicate);
BLELongCharacteristic gyroZChar("0203", BLERead | BLENotify); //| BLEIndicate);
BLELongCharacteristic magXChar("0021", BLERead | BLENotify); //| BLEIndicate);
BLELongCharacteristic magYChar("0022", BLERead | BLENotify); //| BLEIndicate);
BLELongCharacteristic magZChar("0023", BLERead | BLENotify); //| BLEIndicate);

//BLEDevice central;


void setup() {
  // put your setup code here, to run once:
  pinMode(saveLED, OUTPUT);
  pinMode(sendLED, OUTPUT);
  pinMode(saveButton, INPUT);
  pinMode(sendButton, INPUT);
  
  Serial.begin(9600);
  
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
  
  accXService.addCharacteristic(accXChar);
  accYService.addCharacteristic(accYChar);
  accZService.addCharacteristic(accZChar);
  gyroXService.addCharacteristic(gyroXChar);
  gyroYService.addCharacteristic(gyroYChar);
  gyroZService.addCharacteristic(gyroZChar);
  magXService.addCharacteristic(magXChar);
  magYService.addCharacteristic(magYChar);
  magZService.addCharacteristic(magZChar);
  BLE.addService(accXService);
  BLE.addService(accYService);
  BLE.addService(accZService);
  BLE.addService(gyroXService);
  BLE.addService(gyroYService);
  BLE.addService(gyroZService);
  BLE.addService(magXService);
  BLE.addService(magYService);
  BLE.addService(magZService);
  
  BLE.setAdvertisedService(accXService);
  BLE.advertise();
  Serial.println("Advertising...");
}

void loop() {
  BLEDevice central = BLE.central();
  
  if (central) {
    Serial.print("Connected to: ");
    Serial.println(central.address());
    digitalWrite(LED_BUILTIN, HIGH);
  
    while (central.connected()) {
        digitalWrite(sendLED, LOW);
        digitalWrite(saveLED, LOW);
        saveStatus = digitalRead(saveButton);
        if (saveStatus) {
          Serial.println("Starting Save In 3 Seconds!");
          blinkSaveLED(); 
          startSave();
          digitalWrite(saveLED, LOW);
          Serial.println("Saved!");
          delay(100);
        }
    }
  }
  digitalWrite(LED_BUILTIN, LOW);
  Serial.print("Disconnected from: ");
  Serial.println(central.address());
  delay(200);
}


void blinkSaveLED() {
  digitalWrite(saveLED, HIGH);
  delay(500);
  digitalWrite(saveLED, LOW); 
  delay(500); 
  digitalWrite(saveLED,HIGH);
  delay(500);
  digitalWrite(saveLED, HIGH);
  delay(500);
  digitalWrite(saveLED, LOW); 
  delay(500); 
  digitalWrite(saveLED,HIGH);
  delay(500);
}

void startSave() {
  const bool readMag = false;
  const byte captureTimeSecs = 2;
  const unsigned short totalSamples = sampleRates[0] * captureTimeSecs;
  unsigned short samplesRead = 0;
  float imuDataF [totalSamples][9];
  long imuDataL [totalSamples][9]; // = {0, 0, 0, 0, 0, 0, 0, 0, 0};
  
  //Serial.println(totalSamples);
  //bool newSampleRead; 
  
  //do {
  samplesRead = getVals(imuDataF, totalSamples, samplesRead, readMag);
  //Serial.println(samplesRead);
    //Serial.println(samplesRead);
    //delay(100);
  //} while (newSampleRead && (samplesRead != totalSamples)); // getVals return

  if (samplesRead == totalSamples) {
    digitalWrite(saveLED, LOW);
    digitalWrite(sendLED, HIGH);
    bleWrite(imuDataF,imuDataL,totalSamples);
    digitalWrite(sendLED, LOW);
  }
}


// TODO: add timeout based on millis
unsigned short getVals(float dataOut[][9], unsigned short totalSamples, unsigned short sampleNo, bool readMag) {
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

bool bleWrite(float imuDataF[][9], long imuDataL[][9], int totalSamples) {
   for (int i = 0; i < totalSamples; i++) {
    //long message[]
    for (int j = 0; j < 9; j++) {
      float scaled = imuDataF[i][j] * 1000.0;
      imuDataL[i][j] = (long) scaled;
      Serial.print(imuDataL[i][j]);
      Serial.print(",");
    }
   Serial.println();

   accXChar.writeValue(imuDataL[i][0]);
   accYChar.writeValue(imuDataL[i][1]);
   accZChar.writeValue(imuDataL[i][2]);
   delay(10); 
   gyroXChar.writeValue(imuDataL[i][3]);
   gyroYChar.writeValue(imuDataL[i][4]);
   gyroZChar.writeValue(imuDataL[i][5]);
   delay(10);
   magXChar.writeValue(imuDataL[i][6]);
   magYChar.writeValue(imuDataL[i][7]);
   magZChar.writeValue(imuDataL[i][8]);
   delay(10);
   } 
} 
