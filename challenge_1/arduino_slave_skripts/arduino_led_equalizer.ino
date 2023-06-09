// Pins für die LEDs
const int led1Pin = 1;
const int led2Pin = 5;
const int led3Pin = 4;
const int led4Pin = 3;
const int led5Pin = 2;

void setup() {
  Serial.begin(9600);
  pinMode(led1Pin, OUTPUT);
  pinMode(led2Pin, OUTPUT);
  pinMode(led3Pin, OUTPUT);
  pinMode(led4Pin, OUTPUT);
  pinMode(led5Pin, OUTPUT);
}

void loop() {
  if (Serial.available() > 0) {
    char command[3];
    Serial.readBytesUntil('\n', command, 3);

    int led = command[0] - '0';
    int state = command[1] - '0';

    if (led >= 1 && led <= 5) {
      digitalWrite(getLedPin(led), state);
    }
  }
}

int getLedPin(int led) {
  switch (led) {
    case 1:
      return led1Pin;
    case 2:
      return led2Pin;
    case 3:
      return led3Pin;
    case 4:
      return led4Pin;
    case 5:
      return led5Pin;
    default:
      return -1;  // Ungültige LED-Nummer
  }
}
