#include <Arduino_LSM9DS1.h>

#//GLOBALS
const byte d3 = 3;

// PROTOTYPES
//int print_acc();

void setup() {
  // put your setup code here, to run once:
  pinMode(d3, OUTPUT);
  Serial.begin(115200);
  if (!IMU.begin()) {
    Serial.println("Failed to initialize IMU!");
    while (1);
  }
}

void loop() {
  float imu_data[9] = {0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0};
  char sensors[5] = "agm"; // TODO: Add buffer
  digitalWrite(d3, LOW);

  get_vals(imu_data);
  delay(500);
}

int get_vals(float data_out[]) {
  int ready = 1;
  //int values[9] = {0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0};
 
    if (IMU.accelerationAvailable()) {
      IMU.readAcceleration(data_out[0], data_out[1], data_out[2]);
    } 
    else {
      ready = 0;
    }

    if (ready && IMU.gyroscopeAvailable()) {
      IMU.readGyroscope(data_out[3], data_out[4], data_out[5]);
    }
    else {
      ready = 0;
    }
    
    if (ready && IMU.magneticFieldAvailable()) {
      IMU.readMagneticField(data_out[6], data_out[7], data_out[8]);
    }
    else {
      ready = 0;
    }

    if (ready) {
      for (int i = 0; i < 9; i++) {
        Serial.print(data_out[i]);
        Serial.print(",");
      }
      Serial.println();
    }
  return ready;
}
