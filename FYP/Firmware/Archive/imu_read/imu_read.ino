#include <Arduino_LSM9DS1.h>

#//GLOBALS
int D3 = 3;

// PROTOTYPES
//int print_acc();

void setup() {
  // put your setup code here, to run once:
  pinMode(D3, OUTPUT);
  if (!IMU.begin()) {
    Serial.println("Failed to initialize IMU!");
    while (1);
  }
}

void loop() {
  float ax, ay, az, gx, gy, gz, mx, my, mz;
  char sensors[5] = "agm";
  digitalWrite(D3, LOW);

  for (int i = 0; i < 3; i++) {
    get_vals(&ax, &ay, &az, sensors[i]);
  }
  delay(500);
}

int get_vals(float *x, float *y, float *z, char sensor) {
  int ready = 0;
  switch (sensor) {
    case 'a':
      ready = IMU.accelerationAvailable();
      if (ready) {
        IMU.readAcceleration(*x, *y, *z);
        Serial.print("Acc:\t");
      }
      break;

    case 'g':
      ready = IMU.gyroscopeAvailable();
      if (ready) {
        IMU.readGyroscope(*x, *y, *z);
        Serial.print("Gyro:\t");
      }
      break;

    case 'm':
      ready = IMU.magneticFieldAvailable();
      if (ready) {
        IMU.readMagneticField(*x, *y, *z);
        Serial.print("Mag:\t");
      }
      break;

    default:
      break;

  }

  if (ready) {
    //digitalWrite(D3, HIGH);
    Serial.print(*x);
    Serial.print("\t");
    Serial.print(*y);
    Serial.print("\t");
    Serial.print(*z);
    Serial.println();
  }
  return ready;
}
