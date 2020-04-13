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
const byte startLED = 3;
const byte stopLED = 4;
const byte toggleButton = 5;
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


const char* ACTIONS[] = {"standing", "walking", "lying_f", "lying_l", "lying_r", "fall_f", "fall_l", "fall_r"};

#define NUM_ACTIONS (sizeof(ACTIONS) / sizeof(ACTIONS[0]))  //TODO: All below should be defined as macros too
int inputLength;
const byte totalFeatures = 14;
int current_action = 0;
float threshold = 0.85;

const byte sampleLength = 6; //No. of parameters in a single sample (9 if all, 6 w/o magnetometer)
const unsigned short totalSamples = 119; //sampleRates[0] * captureTimeSecs;

byte saveStatus, sendStatus = 0;
byte sampleRates[3] = { 0, 0, 0 }; // {IMU.accelerationSampleRate(), IMU.gyroscopeSampleRate(), IMU.magneticFieldSampleRate()};

unsigned long timer1 = 0;
unsigned long timer2 = 0;
//BLE

BLEService predictionService("e77f260c-813a-4f0b-bb63-4e4ee0c3a103");
BLEByteCharacteristic predictionChar("f29c6ec0-13ef-4266-9fb7-b32c0feec1b3", BLERead | BLENotify);

BLEService startingStreamService("05b7f95e-0d89-43da-973c-3aa5a67b6031");
BLEBoolCharacteristic startingStreamChar("20b35680-9cf5-4f41-bde9-308abbc3c019", BLERead | BLENotify);

BLEService sendDataService("ab36b3d9-12e4-4922-ac94-8873e8252045");
BLEBoolCharacteristic sendDataChar("976aca21-135a-4dfa-b548-68308f7acceb", BLERead | BLEWrite);

/* BLEService dataReadyService("a34984b9-7b89-4553-aced-242a0b289bbc");
BLEBoolCharacteristic dataReadyChar("4174c433-4064-4349-bfa2-009a432a24a4", BLERead | BLENotify);

BLEService imuService("f9dd156e-f108-4139-925c-dd1f157cffa0");
BLECharacteristic imuChar("41277a1b-b4f8-4ddc-871a-db0dd23a3a31", BLERead | BLEIndicate, packetSize); */


void setup() {
    // put your setup code here, to run once:
    pinMode(startLED, OUTPUT);
    pinMode(stopLED, OUTPUT);
    pinMode(toggleButton, INPUT);

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

   
    predictionService.addCharacteristic(predictionChar);
    startingStreamService.addCharacteristic(startingStreamChar);
    sendDataService.addCharacteristic(sendDataChar);
   
    BLE.addService(predictionService);
    BLE.addService(startingStreamService);
    BLE.addService(sendDataService);

    BLE.setAdvertisedService(predictionService);
    BLE.setConnectionInterval(0x0006, 0x0028); // 0x0320);
    BLE.advertise();


    /* Pull in only the operation implementations we need.
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
        tflite::ops::micro::Register_SOFTMAX()); */

    // get the TFL representation of the model byte array
    tflModel = tflite::GetModel(SMVNeuralNet_ReLU_tflite);
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
    Serial.println(inputLength);

}

void loop() {
    digitalWrite(startLED, LOW);
    digitalWrite(stopLED, LOW);
    long imuDataL[sampleLength][totalSamples];
    float smv [totalFeatures];
    initialiseData(imuDataL, smv);
    bool dataReady = 0;
    byte externalStart = 0;
    BLEDevice central = BLE.central();

    if (central) {
        Serial.print("Connected to: ");
        Serial.println(central.address());
        digitalWrite(LED_BUILTIN, HIGH);
        digitalWrite(startLED, LOW);
        digitalWrite(stopLED, LOW);
        predictionChar.writeValue(0);
        sendDataChar.writeValue(0);
        startingStreamChar.writeValue(0);

        while (central.connected()) {

            sendDataChar.readValue(externalStart);
            bool startStream = externalStart || digitalRead(toggleButton);
            bool stopStream = 1;

            if (startStream) {
                startingStreamChar.writeValue(1);
                stopStream = 0;
                blinkLED(startLED, 500, 1);
            }

            while (!stopStream && central.connected()) {
                
                dataReady = startSave(imuDataL, smv);
                sendDataChar.writeValue(1);

                if (dataReady) {
                    current_action = interpret(smv);
                    predictionChar.writeValue(current_action);
                    //Serial.print("Prediction: ");
                    //Serial.println(ACTIONS[current_action]);
                }

                sendDataChar.readValue(externalStart);
                stopStream = digitalRead(toggleButton);

                if ((!dataReady || stopStream) || !externalStart) {
                    Serial.println("Stopping stream...");
                    sendDataChar.writeValue(0);
                    startingStreamChar.writeValue(0);
                    digitalWrite(startLED, LOW);
                    blinkLED(stopLED, 500, 0);
                    initialiseData(imuDataL, smv);
                    stopStream = 1;
                }
                else {
                    initialiseSMV(smv);
                    delay(50);
                }       
            }
        }
    }

    digitalWrite(LED_BUILTIN, LOW);
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

    initialiseSMV(smv);
}

void initialiseSMV(float smv[totalFeatures]) {
    for (int i = 0; i < totalFeatures; i++) { smv[i] = 0.0; }
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


bool startSave(long imuDataL[sampleLength][totalSamples], float smv[totalFeatures]) {
    unsigned short samplesRead = 0;
    float imuDataF[sampleLength][totalSamples];
    bool success = 0;

    //initialiseData(imuDataL, smv);
    samplesRead = getVals(imuDataF, samplesRead);

    if (samplesRead == totalSamples) {
        success = saveData(imuDataF, imuDataL, smv);
    }

    return success;
}

unsigned short getVals(float dataOut[sampleLength][totalSamples], unsigned short sampleNo) {
    int minSamplePeriod = 1000 / sampleRates[0];

    while (sampleNo != totalSamples && IMU.accelerationAvailable() && IMU.gyroscopeAvailable()) {
        IMU.readAcceleration(dataOut[0][sampleNo], dataOut[1][sampleNo], dataOut[2][sampleNo]);
        IMU.readGyroscope(dataOut[3][sampleNo], dataOut[4][sampleNo], dataOut[5][sampleNo]);
        sampleNo++;
        // Serial.println(sampleNo);
        delay(minSamplePeriod);
    }
    //Serial.println("Done");
    return sampleNo;
}

bool saveData(float imuDataF[sampleLength][totalSamples], long imuDataL[sampleLength][totalSamples], float smv[totalFeatures]) {
    Serial.println("Pre-processing raw data...");
    int totalRead = 0;
    for (int i = 0; i < sampleLength; i++) {
        for (int j = 0; j < totalSamples; j++) {
            float scaled = imuDataF[i][j] * 1000.0;
            imuDataL[i][j] = (long)scaled;
            //imuChar.writeValue(imuDataL[i][j]);
            totalRead++;
            //Serial.print(imuDataL[i][j]);
            //Serial.print(",");
        }    
    }

    if (totalRead == (totalSamples * sampleLength)) {
        for (int i = 0; i < 6; i++) {
            if (i < 3) { updateStdMean(imuDataL[i], totalSamples, 4, &smv[i], &smv[i + 6]); }
            else { updateStdMean(imuDataL[i], totalSamples, 2000, &smv[i], &smv[i + 6]); }
        }

        smv[12] = sqrt(pow(smv[6], 2) + pow(smv[7], 2) + pow(smv[8], 2));
        smv[13] = sqrt(pow(smv[9], 2) + pow(smv[10], 2) + pow(smv[11], 2));
        //print_smv(smv);
        return 1;
    }
    else {
        return 0;
    }
}

void print_smv(float smv[totalFeatures]) {
    Serial.print("\n");
    for (int i = 0; i < 14; i++) {
        Serial.print(smv[i], 6);
        Serial.print(", ");
    }
    Serial.print("\n");
}
int interpret(float smv[totalFeatures]) {
    Serial.println("Predicting...");

    tflInputTensor->data.f = smv;
    TfLiteStatus invokeStatus = tflInterpreter->Invoke();
    if (invokeStatus != kTfLiteOk) {
        Serial.println("Invoke failed!");
        // while (1);
        return 0;
    }
    float max = 0.0;
    int max_index = current_action;

    for (int i = 0; i < 8; i++) {
        float prediction = tflOutputTensor->data.f[i];
        
        /*Serial.print(ACTIONS[i]);
        Serial.print(": ");
        Serial.println(prediction, 6);*/

        if (prediction > threshold) {
            max_index = i;
        }
    }
    Serial.println();
    return max_index;
}