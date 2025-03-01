#include <HX711.h>
HX711 scale;

const int LOADCELL_DOUT_PIN = 2;
const int LOADCELL_SCK_PIN = 3;
const float CALIBRATION_FACTOR = -7050; // Calibrate for your sensor

void setup() {
  Serial.begin(9600);
  scale.begin(LOADCELL_DOUT_PIN, LOADCELL_SCK_PIN);
  scale.set_scale(CALIBRATION_FACTOR);
  scale.tare();
}

void loop() {
  if (scale.is_ready()) {
    float weight = scale.get_units(10);
    Serial.println(weight);
  }
  delay(1000);
}
