#include <SPI.h>
#include <MFRC522.h>

#define SS_PIN 10
#define RST_PIN 9
#define LED_PIN 7 //Das Wort „LED“ steht jetzt für den Wert 9.

int helligkeit= 0; //Das Wort „helligkeit“ steht nun für den Wert, der bei der PWM ausgegeben wird. Die Zahl 0 ist dabei nur ein beliebiger Startwert.


MFRC522 rfid(SS_PIN, RST_PIN);   // RFID-Objekt erstellen

void setup() {
  pinMode(LED_PIN, OUTPUT);
  Serial.begin(9600);    // Serielle Kommunikation starten
  SPI.begin();           // SPI-Bus starten
  rfid.PCD_Init();       // RFID-Reader initialisieren
}

void loop() {
  // RFID-Karte oder -Tag erkennen
  if (rfid.PICC_IsNewCardPresent() && rfid.PICC_ReadCardSerial()) {
    String rfidData = "";
    digitalWrite(LED_PIN, HIGH);
    // RFID-Daten auslesen
    for (byte i = 0; i < rfid.uid.size; i++) {
      rfidData += String(rfid.uid.uidByte[i] < 0x10 ? "0" : "");
      rfidData += String(rfid.uid.uidByte[i], HEX);
    }
    digitalWrite(LED_PIN, LOW); 

    // RFID-Daten über die serielle Schnittstelle senden
    Serial.println(rfidData);
    rfid.PICC_HaltA();   // PICC (Proximity Integrated Circuit Card) anhalten
  }
}