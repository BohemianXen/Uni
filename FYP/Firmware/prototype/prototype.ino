/**
* @file prototype.ino
*
* Firmware for the prototype device. Uses on-board AI inference for fall detection.
*
* @author Ralph Mukusa
* contact: ralph.mukusa@gmail.com
*
* version: 1.0
**/


/*----------------------------------------------------- INCLUDES --------------------------------------------------*/

// Standard libs
#include "math.h"

// Arduino libs
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

// My libs
#include "stats.h"
#include "model.h"


/*----------------------------------------------------- GLOBALS ---------------------------------------------------*/

#define THRESHOLD 0.85  // Inference threshold required to confirm a prediction

#define STREAM_LED 3
#define STOP_LED 4
#define RECORD_BUTTON 5


/** 
* TensorFlow Lite (Micro) globals.
* Following snippet as given for public use by Don Coleman and Sandeep Mistry.
* Available: https://github.com/arduino/ArduinoTensorFlowLiteTutorials/blob/master/GestureToEmoji/ArduinoSketches/IMU_Classifier/IMU_Classifier.ino
**/
tflite::MicroErrorReporter tflErrorReporter;
tflite::ops::micro::AllOpsResolver tflOpsResolver;
const tflite::Model* tflModel = nullptr;
tflite::MicroInterpreter* tflInterpreter = nullptr;
TfLiteTensor* tflInputTensor = nullptr;
TfLiteTensor* tflOutputTensor = nullptr;

// Create a static memory buffer for TFLM, the size may need to be adjusted based on the model
constexpr int tensorArenaSize = 60 * 1024;
byte tensorArena[tensorArenaSize];

/* End of TFLite snippet */

const char* ACTIONS[] = {"standing", "walking", "lying_f", "lying_l", "lying_r", "fall_f", "fall_l", "fall_r"};
#define NUM_ACTIONS (sizeof(ACTIONS) / sizeof(ACTIONS[0]))
byte currentAction = 0;  // Holds the current predicted action in index form
const byte totalFeatures = 14;
int inputLength;

const byte sampleLength = 6; // No. of parameters in a single sample (9 if all, 6 w/o magnetometer)
const unsigned short totalSamples = 119; // 1s capture given 119Hz sampling frequency
byte sampleRates[3] = { 0, 0, 0 };

/* ------------------------------------------------------- BLE -----------------------------------------------------*/

BLEService predictionService("e77f260c-813a-4f0b-bb63-4e4ee0c3a103");
BLEByteCharacteristic predictionChar("f29c6ec0-13ef-4266-9fb7-b32c0feec1b3", BLERead | BLENotify);

BLEService startingStreamService("05b7f95e-0d89-43da-973c-3aa5a67b6031");
BLEBoolCharacteristic startingStreamChar("20b35680-9cf5-4f41-bde9-308abbc3c019", BLERead | BLENotify);

BLEService sendDataService("ab36b3d9-12e4-4922-ac94-8873e8252045");
BLEBoolCharacteristic sendDataChar("976aca21-135a-4dfa-b548-68308f7acceb", BLERead | BLEWrite);

/*------------------------------------------------------- SETUP ----------------------------------------------------*/
/**
* Arduino setup function. Runs on initial boot and resets.
**/
void setup() {
    pinMode(STREAM_LED, OUTPUT);
    pinMode(STOP_LED, OUTPUT);
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
        while (1);
    }

    // Name device then add BLE Services and Characteristics
    BLE.setLocalName("FallDetector");
    BLE.setDeviceName("FallDetector");

    predictionService.addCharacteristic(predictionChar);
    startingStreamService.addCharacteristic(startingStreamChar);
    sendDataService.addCharacteristic(sendDataChar);
   
    BLE.addService(predictionService);
    BLE.addService(startingStreamService);
    BLE.addService(sendDataService);
    BLE.setAdvertisedService(predictionService);

    // Ask central to poll more frequently (1.25ms(6, 40)) 
    BLE.setConnectionInterval(0x0006, 0x0028);
    BLE.advertise();


     /**
     * TensorFlow Lite (Micro) inits
     * Following snippet adapted from code available for public use.
     * Authors: Don Coleman and Sandeep Mistry.
     * Available: https://github.com/arduino/ArduinoTensorFlowLiteTutorials/blob/master/GestureToEmoji/ArduinoSketches/IMU_Classifier/IMU_Classifier.ino
     **/
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
   
    /* End of TFLite snippet */
}

/*----------------------------------------------------- MAIN LOOP --------------------------------------------------*/
/**
* Arduino main loop function.
**/

void loop() {
    // Inits
    digitalWrite(STREAM_LED, LOW);
    digitalWrite(STOP_LED, LOW);
    long imuDataL[sampleLength][totalSamples];
    float smv [totalFeatures];  // Array for Signal Magnitude Vectors (SMV) model inputs
    initialiseData(imuDataL, smv);
    bool dataReady = 0;
    byte externalStart = 0;  // Used for signalling a received start from the UI
    BLEDevice central = BLE.central();

    if (central) {
        Serial.print("Connected to: ");
        Serial.println(central.address());
        digitalWrite(LED_BUILTIN, HIGH);
        digitalWrite(STREAM_LED, LOW);
        digitalWrite(STOP_LED, LOW);

        // Update characteristics
        predictionChar.writeValue(0);
        sendDataChar.writeValue(0);
        startingStreamChar.writeValue(0);

        while (central.connected()) {
            sendDataChar.readValue(externalStart);
            bool startStream = externalStart || digitalRead(RECORD_BUTTON); // Check if start initiated through app or button
            bool stopStream = 1;

            if (startStream) {
                startingStreamChar.writeValue(1);
                stopStream = 0;
                blinkLED(STREAM_LED, 500, HIGH);
            }

            while (!stopStream && central.connected()) {
                dataReady = startSave(imuDataL, smv);
                sendDataChar.writeValue(1);

                if (dataReady) {
                    currentAction = interpret(smv);  // Predict action 
                    predictionChar.writeValue(currentAction);
                    //Serial.print("Prediction: ");
                    //Serial.println(ACTIONS[currentAction]);
                }

                stopStream = digitalRead(RECORD_BUTTON);

                if (!dataReady || stopStream) {
                    Serial.println("Stopping stream...");
                    sendDataChar.writeValue(0);
                    startingStreamChar.writeValue(0);
                    digitalWrite(STREAM_LED, LOW);
                    blinkLED(STOP_LED, 500, LOW);
                    initialiseData(imuDataL, smv);
                    stopStream = 1;
                }
                else {
                    initialiseSMV(smv);  // Reset tensor input values
                    delay(50);
                }       
            }
        }
    }

    // Client has disconnected
    digitalWrite(LED_BUILTIN, LOW);
    Serial.print("Disconnected from: ");
    Serial.println(central.address());
    delay(200);
}

/**
 * Initialises the 2D long array with all zeros as well as the 1D model input float array.
 *
 * @param long** imuDataL: 2D array holding the scaled IMU readings.
 * @param float* smv: 1D array holding the model input values.
**/
void initialiseData(long imuDataL[sampleLength][totalSamples], float smv[totalFeatures]) {
    for (int i = 0; i < sampleLength; i++) {
        for (int j = 0; j < totalSamples; j++) {
            imuDataL[i][j] = 0;
        }
    }

    initialiseSMV(smv);
}


/**
 * Initialises the 1D model input float array.
 *
 * @param float* smv: 1D array holding the model input values.
**/
void initialiseSMV(float smv[totalFeatures]) {
    for (int i = 0; i < totalFeatures; i++) { smv[i] = 0.0; }
}


/**
 * Blinks an LED 6 times at the requested frequency.
 *
 * @param int LED: The digital pin number of the LED to be toggled.
 * @param int period: The blinking interval.
 * @param int end: The desired end state of the LED, either HIGH(1) or LOW(0).
**/
void blinkLED(int LED, int period, int end) {
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
 * @param float* smv: 1D array holding the model input values.
 * @return bool: Whether or not all samples were successfully recorded.
**/
bool startSave(long imuDataL[sampleLength][totalSamples], float smv[totalFeatures]) {
    // Inits
    float imuDataF[sampleLength][totalSamples];  // IMU module saves as float
    bool success = 0;

    unsigned short samplesRead = getVals(imuDataF);

    if (samplesRead == totalSamples) {
        success = saveData(imuDataF, imuDataL, smv);
    }

    return success;
}


/**
 * Reads the Acc and Gyro, storing the values in the passed array.
 *
 * @param float** dataOut: 2D float array where the IMU readings will be stored.
 * @return unsigned short: Number of samples successfully read.
**/
unsigned short getVals(float dataOut[sampleLength][totalSamples]) {
    unsigned short sampleNo = 0;
    int minSamplePeriod = 1000 / sampleRates[0];  // Cap read rate to ensure new samples will always be available

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


/**
 * Scales the float IMU reading into longs then uses this to calculate the model input values.
 *
 * @param float** imuDataF: 2D float array holding the IMU readings as floats.
 * @param long** imuDataL: 2D float array holding the IMU readings as scaled longs.
 * @param float* smv: 1D array holding the model input values.
 * @return bool: Whether or not all samples were successfully converted, copied, and utilised for input calculations.
**/
bool saveData(float imuDataF[sampleLength][totalSamples], long imuDataL[sampleLength][totalSamples], float smv[totalFeatures]) {
    Serial.println("Pre-processing raw data...");
    int totalRead = 0;
    for (int i = 0; i < sampleLength; i++) {
        for (int j = 0; j < totalSamples; j++) {
            float scaled = imuDataF[i][j] * 1000.0;  // Scale floats
            imuDataL[i][j] = (long)scaled;
            totalRead++;

            /* DEBUG ONLY imuChar.writeValue(imuDataL[i][j]); 
            Serial.print(imuDataL[i][j]);
            Serial.print(",");*/
        }    
    }

    if (totalRead == (totalSamples * sampleLength)) {

        // Calculate the statistics and store them in the input array
        for (int i = 0; i < 6; i++) {
            if (i < 3) { updateStdMean(imuDataL[i], totalSamples, 4, &smv[i], &smv[i + 6]); }
            else { updateStdMean(imuDataL[i], totalSamples, 2000, &smv[i], &smv[i + 6]); }
        }

        smv[12] = sqrt(pow(smv[6], 2) + pow(smv[7], 2) + pow(smv[8], 2));  // Magnitude of axial acc means
        smv[13] = sqrt(pow(smv[9], 2) + pow(smv[10], 2) + pow(smv[11], 2));  // Magnitude of axial gyro means
        //print_smv(smv); FOR DEBUG
        return 1;
    }
    else {
        return 0;
    }
}


/**
 * Prints the model input values.
 *
 * @param float* smv: 1D array holding the model input values.
**/
void print_smv(float smv[totalFeatures]) {
    Serial.print("\n");
    for (int i = 0; i < 14; i++) {
        Serial.print(smv[i], 6);
        Serial.print(", ");
    }
    Serial.print("\n");
}


/**
 * Infer the current action based on the current model input array.
 *
 * @param float* smv: 1D array holding the model input values.
 * @return byte: Index of the current predicted action. 
**/
byte interpret(float smv[totalFeatures]) {
    Serial.println("Predicting...");

    tflInputTensor->data.f = smv;  // Assign input array to mpdel input tensor
    
    // Attempt to invoke
    TfLiteStatus invokeStatus = tflInterpreter->Invoke();
    if (invokeStatus != kTfLiteOk) {
        Serial.println("Invoke failed!");
        return 0;
    }

    float max = 0.0;  // Highest model output encountered (i.e. the greatest probability) 
    byte max_index = currentAction;  // Index of best guess

    for (int i = 0; i < NUM_ACTIONS; i++) {
        // Get prediction at each index of output tensor and update only if probability threshold is exceeded
        float prediction = tflOutputTensor->data.f[i];  
        if (prediction > THRESHOLD) { max_index = i; }

        /* DEBUG ONLY Serial.print(ACTIONS[i]);
        Serial.print(": ");
        Serial.println(prediction, 6);
        Serial.println();*/
    }
   
    return max_index;
}
