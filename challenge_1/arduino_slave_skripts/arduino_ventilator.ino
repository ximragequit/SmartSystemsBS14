// Pin für den Ventilator
const int ventilatorPin = 9;

// Befehl zum Ein- und Ausschalten des Ventilators
const char commandOn = '1';
const char commandOff = '0';

void setup() {
  Serial.begin(9600);
  pinMode(ventilatorPin, OUTPUT);
}

void loop() {
  if (Serial.available() > 0) {
    char command = Serial.read();

    if (command == commandOn) {
      digitalWrite(ventilatorPin, HIGH);  // Ventilator einschalten
    } else if (command == commandOff) {
      digitalWrite(ventilatorPin, LOW);   // Ventilator ausschalten
    }
  }
}
