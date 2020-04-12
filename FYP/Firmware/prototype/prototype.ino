#include "stats.h"
#include "math.h"

#include <Arduino_LSM9DS1.h>
#include <ArduinoBLE.h>

#include <TensorFlowLite.h>
#include "tensorflow/lite/experimental/micro/kernels/micro_ops.h"
#include <tensorflow/lite/experimental/micro/kernels/all_ops_resolver.h>
#include <tensorflow/lite/experimental/micro/micro_error_reporter.h>
#include <tensorflow/lite/experimental/micro/micro_interpreter.h>
#include "tensorflow/lite/experimental/micro/micro_mutable_op_resolver.h"
#include <tensorflow/lite/schema/schema_generated.h>
#include <tensorflow/lite/version.h>

#include "model.h"

#//GLOBALS
const byte saveLED = 3;
const byte sendLED = 4;
const byte saveButton = 5;
const byte sendButton = 6;

// global variables used for TensorFlow Lite (Micro)
tflite::MicroErrorReporter tflErrorReporter;

// pull in all the TFLM ops, you can remove this line and
// only pull in the TFLM ops you need, if would like to reduce
// the compiled size of the sketch.
tflite::ops::micro::AllOpsResolver tflOpsResolver;

const tflite::Model* tflModel = nullptr;
tflite::MicroInterpreter* tflInterpreter = nullptr;
TfLiteTensor* tflInputTensor = nullptr;
TfLiteTensor* tflOutputTensor = nullptr;

// Create a static memory buffer for TFLM, the size may need to
// be adjusted based on the model you are using
constexpr int tensorArenaSize = 60 * 1024;
byte tensorArena[tensorArenaSize];


const char* GESTURES[] = {
  "punch",
  "flex"
};

#define NUM_GESTURES (sizeof(GESTURES) / sizeof(GESTURES[0]))  //TODO: All below should be defined as macros too

int inputLength;
const byte totalFeatures = 14;
const byte sampleLength = 6; //No. of parameters in a single sample (9 if all, 6 w/o magnetometer)
const byte packetLength = 8; // No. of samples in a single data packet
const unsigned short packetSize = sampleLength * packetLength * 4; // No. of bytes in an entire packet
//const unsigned long debounceTime = 1000;
const unsigned short totalSamples = 119; //sampleRates[0] * captureTimeSecs;
const unsigned short totalPackets = totalSamples / packetLength; //TODO: What do to if float result
byte saveStatus, sendStatus = 0;
byte sampleRates[3] = { 0, 0, 0 }; // {IMU.accelerationSampleRate(), IMU.gyroscopeSampleRate(), IMU.magneticFieldSampleRate()};

unsigned long timer1 = 0;
unsigned long timer2 = 0;
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
    }
    else {
        sampleRates[0] = IMU.accelerationSampleRate();
        sampleRates[1] = IMU.gyroscopeSampleRate();
        sampleRates[2] = IMU.magneticFieldSampleRate();
    }


    if (!BLE.begin()) {
        Serial.println("Failed to initialise BT Module");
        while (1);
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
    BLE.setConnectionInterval(0x0006, 0x0028); // 0x0320);
    BLE.advertise();


    // Pull in only the operation implementations we need.
    // This relies on a complete list of all the ops needed by this graph.
    // An easier approach is to just use the AllOpsResolver, but this will
    // incur some penalty in code space for op implementations that are not
    // needed by this graph.
    static tflite::MicroMutableOpResolver micro_mutable_op_resolver;  // NOLINT
    //micro_mutable_op_resolver.AddBuiltin(tflite::BuiltinOperator_TANH,
    //    tflite::ops::micro::Register_TANH());
    micro_mutable_op_resolver.AddBuiltin(tflite::BuiltinOperator_RELU,
        tflite::ops::micro::Register_RELU());
    micro_mutable_op_resolver.AddBuiltin(tflite::BuiltinOperator_SOFTMAX,
        tflite::ops::micro::Register_SOFTMAX());

    // get the TFL representation of the model byte array
    tflModel = tflite::GetModel(model);
    if (tflModel->version() != TFLITE_SCHEMA_VERSION) {
        Serial.println("Model schema mismatch!");
        while (1);
    }

    // Create an interpreter to run the model
    tflInterpreter = new tflite::MicroInterpreter(tflModel, tflOpsResolver, tensorArena, tensorArenaSize, &tflErrorReporter);

    // Allocate memory for the model's input and output tensors
    tflInterpreter->AllocateTensors();

    // Get pointers for the model's input and output tensors
    tflInputTensor = tflInterpreter->input(0);
    tflOutputTensor = tflInterpreter->output(0);

    inputLength = tflInputTensor->bytes / sizeof(float);

}

void loop() {
    long imuDataL[sampleLength][totalSamples];
    float smv [totalFeatures];
    initialiseData(imuDataL, smv);
    bool dataReady = 0;
    byte external_start = 0;
    BLEDevice central = BLE.central();

    if (central) {
        Serial.print("Connected to: ");
        Serial.println(central.address());
        digitalWrite(LED_BUILTIN, HIGH);
        digitalWrite(sendLED, HIGH);
        dataReadyChar.writeValue(0);
        sendDataChar.writeValue(0);
        startingStreamChar.writeValue(0);

        while (central.connected()) {
            //digitalWrite(saveLED, LOW);

            //external_start = 0;
            sendDataChar.readValue(external_start);
            delay(100);
            bool startStream = external_start || digitalRead(saveButton);
            bool stopStream = 1;

            while (!stopStream && central.connected()) {
                dataReady = startSave(imuDataL, smv);
                //dataReadyChar.writeValue(dataReady);
                //digitalWrite(saveLED, LOW);
                //delay(100);
                //bool dataSent = sendData(imuDataL);
                if (dataReady) {
                    int guess = interpret(smv);
                }
                stopStream = digitalRead(saveButton);
                if (stopStream) {
                    dataReadyChar.writeValue(0);
                    sendDataChar.writeValue(0);
                    startingStreamChar.writeValue(0);
                    digitalWrite(saveLED, HIGH);
                    delay(1000);
                }
                delay(10);
            }
        }
    }

    digitalWrite(LED_BUILTIN, LOW);
    digitalWrite(sendLED, LOW);
    digitalWrite(saveLED, LOW);
    Serial.print("Disconnected from: ");
    Serial.println(central.address());
    delay(200);
}

void initialiseData(long imuDataL[sampleLength][totalSamples], float smv[totalFeatures]) {
    for (int i = 0; i < sampleLength; i++) {
        for (int j = 0; j < totalSamples; j++) {
            imuDataL[i][j] = 0;
        }
    }

    for (int i = 0; i < totalFeatures; i++) { smv[i] = 0.0; }   
}


void blinkSaveLED(int period) {
    digitalWrite(saveLED, HIGH);
    delay(period);
    digitalWrite(saveLED, LOW);
    delay(period);
    digitalWrite(saveLED, HIGH);
    delay(period);
    digitalWrite(saveLED, LOW);
    delay(period);
    digitalWrite(saveLED, HIGH);
    delay(period);
    digitalWrite(saveLED, LOW);
    delay(period);
    if (period == 500) { digitalWrite(saveLED, HIGH); }
}

bool startSave(long imuDataL[sampleLength][totalSamples], float smv[totalFeatures]) {
    const byte captureTimeSecs = 2;
    unsigned short samplesRead = 0;
    float imuDataF[sampleLength][totalSamples];
    bool success = 0;

    //initialiseData(imuDataL, smv);
    samplesRead = getVals(imuDataF, samplesRead);

    if (samplesRead == totalSamples) {
        //digitalWrite(saveLED, LOW);
        //digitalWrite(sendLED, HIGH);

        success = saveData(imuDataF, imuDataL, smv);

        if (!success) { blinkSaveLED(50); }
    }

    return success;
}

unsigned short getVals(float dataOut[sampleLength][totalSamples], unsigned short sampleNo) {

    while (sampleNo != totalSamples && IMU.accelerationAvailable() && IMU.gyroscopeAvailable()) {
        IMU.readAcceleration(dataOut[0][sampleNo], dataOut[1][sampleNo], dataOut[2][sampleNo]);
        IMU.readGyroscope(dataOut[3][sampleNo], dataOut[4][sampleNo], dataOut[5][sampleNo]);
        sampleNo++;
    }
    // Serial.println("Done");
    return sampleNo;
}

bool saveData(float imuDataF[sampleLength][totalSamples], long imuDataL[sampleLength][totalSamples], float smv[totalFeatures]) {
    Serial.println("Sending data...");
    int totalRead = 0;
    for (int i = 0; i < sampleLength; i++) {
        for (int j = 0; j < totalSamples; j++) {
            float scaled = imuDataF[i][j] * 1000.0;
            imuDataL[i][j] = (long)scaled;
            //imuChar.writeValue(imuDataL[i][j]);
            totalRead++;
            Serial.print(imuDataL[i][j]);
            Serial.print(",");
        }    
    }

    //Serial.println(totalRead);
    if (totalRead == (totalSamples * sampleLength)) {
        for (int i = 0; i < 3; i++) {
            updateStdMean(imuDataL[i], totalSamples, 4, &smv[i], &smv[i+6]);
        }

        for (int i = 3; i < 6; i++) {
            updateStdMean(imuDataL[i], totalSamples, 2000, &smv[i], &smv[i+6]);
        }

        smv[12] = sqrt(pow(smv[6], 2) + pow(smv[7], 2) + pow(smv[8], 2));
        smv[13] = sqrt(pow(smv[9], 2) + pow(smv[10], 2) + pow(smv[11], 2));

        return 1;
    }
    else {
        return 0;
    }
}

int interpret(float smv[totalFeatures]) {
    tflInputTensor->data.f = smv;
    TfLiteStatus invokeStatus = tflInterpreter->Invoke();
    if (invokeStatus != kTfLiteOk) {
        Serial.println("Invoke failed!");
        //while (1);
        return 0;
    }
    for (int i = 0; i < totalFeatures; i++) {
        //Serial.print(GESTURES[i]);
        //Serial.print(": ");
        Serial.println(tflOutputTensor->data.f[i]); // , 14);
    }
    Serial.println();
    return 1;
}