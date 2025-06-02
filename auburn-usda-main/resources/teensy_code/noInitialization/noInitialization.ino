
// This function executes exactly once at start up
void setup() {
  Serial.begin(9600);
}

// This repeats as long as the device is powered on
void loop() {
  Serial.println("O," + String(random(400)) + "," + String(random(400)));
  delay(100);

}
