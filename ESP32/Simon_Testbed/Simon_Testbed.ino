void setup() {
  // Initialize serial communication
  Serial.begin(115200);  // Use the same baud rate as in the Python script
  pinMode(5, OUTPUT);
    digitalWrite(5, 1);

}

void loop() {
  if (Serial.available() > 0) {
    // Read the data from the serial port
    char receivedChar = Serial.read();

    // Process the received data (0 or 1)
    if (receivedChar == '0') {
      digitalWrite(5,1);
    } else if (receivedChar == '1') {
      digitalWrite(5, 0);
    }
  }

  // Add your other code here
}
