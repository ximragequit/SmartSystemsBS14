#include <DHT.h>

#define DHTPIN 2       // Pin, an dem der DHT11-Sensor angeschlossen ist
#define DHTTYPE DHT11   // Verwendeter DHT-Typ

DHT dht(DHTPIN, DHTTYPE);

void setup() {
  Serial.begin(9600);
  dht.begin();
}

void loop() {
  delay(2000);  // Warte 2 Sekunden zwischen den Messungen

  float temperature = dht.readTemperature();       // Temperatur auslesen
  float humidity = dht.readHumidity();             // Luftfeuchtigkeit auslesen

  if (isnan(temperature) || isnan(humidity)) {
    Serial.println("Fehler beim Auslesen des DHT-Sensors!");
    return;
  }

  Serial.println(temperature);
}
