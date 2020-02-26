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
BLEService imuService("f9dd156e-f108-4139-925c-dd1f157cffa0");
BLELongCharacteristic imuChar("41277a1b-b4f8-4ddc-871a-db0dd23a3a31", BLERead | BLENotify); //| BLEIndicate);

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
  
  imuService.addCharacteristic(imuChar);
  BLE.addService(imuService);
  
  BLE.setAdvertisedService(imuService);
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
   Serial.println("Sending data...");
   for (int i = 0; i < totalSamples; i++) {
    //byte buff[36];
    //long shift = 0;
    for (int j = 0; j < 9; j++) {
      float scaled = imuDataF[i][j] * 1000.0;
      imuDataL[i][j] = (long) scaled;
      imuChar.writeValue(imuDataL[i][j]);
      Serial.print(imuDataL[i][j]);
      Serial.print(",");
    }
    Serial.println();
    //delay(10);
   } 
} 
