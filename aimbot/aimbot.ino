#include <Servo.h>

Servo servo1;
Servo servo2;
String inputString = "";  // A String to hold incoming data
boolean stringComplete = false;  // Whether the string is complete

void setup() {
  Serial.begin(9600);
  servo1.attach(9);  // Attach servo1 to pin 9
  servo2.attach(10); // Attach servo2 to pin 10
  inputString.reserve(200);  // Reserve 200 bytes for the inputString
}

void loop() {
  // Process the input string when it's complete
  if (stringComplete) {
    processInput();
    inputString = "";
    stringComplete = false;
  }
}

void serialEvent() {
  while (Serial.available()) {
    // Get the new byte:
    char inChar = (char)Serial.read();
    // Add it to the inputString:
    inputString += inChar;
    // If the incoming character is a newline, set a flag
    // so the main loop can process it:
    if (inChar == '\n') {
      stringComplete = true;
    }
  }
}

void processInput() {
  int speeds[20];  // Adjust size as needed
  int speedCount = 0;
  char* strtokIndx;  // This is used by strtok() as an index

  // Convert the string to a char array
  char inputArray[200];
  inputString.toCharArray(inputArray, 200);

  // Split the input string by commas
  strtokIndx = strtok(inputArray, ",");  // Get the first speed
  while (strtokIndx != NULL) {
    speeds[speedCount++] = atoi(strtokIndx);  // Convert speed to int and store it
    strtokIndx = strtok(NULL, ",");  // Get the next speed
  }

  // Process pairs of speeds
  for (int i = 0; i < speedCount; i += 2) {
    if (i + 1 < speedCount) {  // Ensure there's a pair
      int speed1 = speeds[i];
      int speed2 = speeds[i + 1];
      if (speed1 >= 0 && speed1 <= 180 && speed2 >= 0 && speed2 <= 180) {
        servo1.write(speed1);
        servo2.write(speed2);
      }
    }
  }
}
