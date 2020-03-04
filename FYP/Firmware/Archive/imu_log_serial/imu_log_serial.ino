#include <Arduino_LSM9DS1.h>

#//GLOBALS
const byte saveLED = 3;
const byte sendLED = 4;
const byte saveButton = 5; 
const byte sendButton = 6;
unsigned long debounceTime = 1000;
//unsigned long 
byte saveStatus, sendStatus = 0;
byte sampleRates [3] = {0, 0, 0}; // {IMU.accelerationSampleRate(), IMU.gyroscopeSampleRate(), IMU.magneticFieldSampleRate()};

// PROTOTYPES
//int print_acc();

void setup() {
  // put your setup code here, to run once:
  pinMode(saveLED, OUTPUT);
  pinMode(sendLED, OUTPUT);
  pinMode(saveButton, INPUT);
  pinMode(sendButton, INPUT);
  
  Serial.begin(115200);
  if (!IMU.begin()) {
    Serial.println("Failed to initialize IMU!");
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
}

void loop() {
  digitalWrite(sendLED, LOW);
  digitalWrite(saveLED, LOW);
  saveStatus = digitalRead(saveButton);
  if (saveStatus) {
    //Serial.println("Starting Save In 3 Seconds!");
    blinkSaveLED(); 
    startSave();
    //digitalWrite(saveLED, LOW);
    //Serial.println("Saved!");
    delay(5000);
  }
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
    serialWrite(imuDataF,imuDataL,totalSamples);
    //digitalWrite(sendLED, LOW);
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
  
  /*if (IMU.accelerationAvailable()) {
    IMU.readAcceleration(dataOut[sampleNo][0], dataOut[sampleNo][1], dataOut[sampleNo][2]);
  } else {
    Serial.println("Acc data not ready!");
    ready = false;
  }

  if (ready && IMU.gyroscopeAvailable()) {
    IMU.readGyroscope(dataOut[sampleNo][3], dataOut[sampleNo][4], dataOut[sampleNo][5]);
  } else {
    Serial.println("Gyro data not ready!");
    ready = false;
  }
  
  if (readMag){
    if (ready && IMU.magneticFieldAvailable()) {
      IMU.readMagneticField(dataOut[sampleNo][6], dataOut[sampleNo][7], dataOut[sampleNo][8]);
    } else {
      //Serial.println("Mag data not ready!");
      ready = false;
    }
  }

    /*if (ready) {
    for (int i = 0; i < 9; i++) {
      //float scaled = dataOut[i] * 1000.0;
       dataOut[sampleNo][i] =  dataOut[i]; // (long) scaled;
      //Serial.print(imuData[sampleNo][i]);
      //Serial.print(",");
    }
    //Serial.println();
    //delay(round(1/sampleRates[0]));
  }
  return sampleNo;
}*/


bool serialWrite(float imuDataF[][9], long imuDataL[][9], int totalSamples) {
   for (int i = 0; i < totalSamples; i++) {
    for (int j = 0; j < 9; j++) {
      float scaled = imuDataF[i][j] * 1000.0;
      imuDataL[i][j] = (long) scaled;
      Serial.print(imuDataL[i][j]);
      Serial.print(",");
    }
    Serial.println();
   }
} 
