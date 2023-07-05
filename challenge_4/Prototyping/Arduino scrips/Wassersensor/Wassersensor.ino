// Pin, an dem der Wassersensor angeschlossen ist
const int waterSensorPin = A0;

void setup() {
  Serial.begin(9600);
}

void loop() {
  // Den Wert vom Wassersensor auslesen
  int sensorValue = analogRead(waterSensorPin);
  
  // Den gelesenen Wert auf der seriellen Schnittstelle ausgeben
  Serial.println(sensorValue);
  // Eine kurze Pause
  delay(1000);
}