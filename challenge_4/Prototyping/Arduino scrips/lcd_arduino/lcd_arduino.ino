#include <LiquidCrystal.h>

// initialize the library by associating any needed LCD interface pin
// with the arduino pin number it is connected to
const int rs = 12, en = 11, d4 = 5, d5 = 4, d6 = 3, d7 = 2;
LiquidCrystal lcd(rs, en, d4, d5, d6, d7);

void setup() {
  // set up the LCD's number of columns and rows:
  lcd.begin(16, 2);
  lcd.clear();
  lcd.print("Arduino LCD");
  Serial.begin(9600);  // Start Serial communication
}

void loop() {
  if (Serial.available() > 0) {
    char command = Serial.read();

    // Befehle vom Raspberry Pi verarbeiten
    if (command == 'C') {
      lcd.clear();
    }
    else if (command == 'M') {
      int column = Serial.parseInt();
      int row = Serial.parseInt();
      lcd.setCursor(column, row);
    }
    else if (command == 'W') {
      String text = Serial.readStringUntil('\n');
      lcd.print(text);
    }
  }
}