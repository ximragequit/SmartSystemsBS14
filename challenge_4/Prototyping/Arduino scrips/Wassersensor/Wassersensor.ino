// Pin, an dem der Wassersensor angeschlossen ist
const int waterSensorPin = A0;

void setup() {
  Serial.begin(9600);
}

void loop() {
  // Den Wert vom Wassersensor auslesen
  int sensorValue = analogRead(waterSensorPin);
  
  // Den gelesenen Wert auf der seriellen Schnittstelle ausgeben
  Serial.print("Sensorwert: ");
  Serial.println(sensorValue);
  
  // Überprüfen des Wasserstands
  if (sensorValue < 500) {
    Serial.println("Wasserstand niedrig");
    // Hier können Aktionen für niedrigen Wasserstand ausgeführt werden
  } else {
    Serial.println("Wasserstand normal");
    // Hier können Aktionen für normalen Wasserstand ausgeführt werden
  }
  
  // Eine kurze Pause
  delay(1000);
}