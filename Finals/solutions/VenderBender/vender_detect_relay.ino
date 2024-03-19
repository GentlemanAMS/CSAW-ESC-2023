volatile bool risingEdgeDetected = false;

void setup() {
  pinMode(2, INPUT);
  attachInterrupt(digitalPinToInterrupt(2), risingEdgeInterrupt, RISING);
  Serial.begin(115200);
}

void loop() {
  if (risingEdgeDetected) {
    Serial.print("E");
    risingEdgeDetected = false;
  }
  // Your other code can go here
}

void risingEdgeInterrupt() {
  risingEdgeDetected = true;
}
