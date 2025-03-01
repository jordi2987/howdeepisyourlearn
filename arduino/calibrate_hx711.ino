#include <HX711.h>
HX711 scale;

void setup() {
  Serial.begin(9600);
  Serial.println("Remove all weight from scale!");
  scale.begin(2, 3);
  scale.set_scale();
  scale.tare();
}

void loop() {
  if (Serial.available()) {
    char cmd = Serial.read();
    if(cmd == 't') scale.tare();
  }
  Serial.print("Raw value: ");
  Serial.println(scale.read());
  delay(100);
}
