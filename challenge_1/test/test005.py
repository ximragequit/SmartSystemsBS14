import smbus
import time

# Adresse des Arduino
arduino_address = 0x08

# I2C-Busnummer (normalerweise 1 auf dem Raspberry Pi)
bus_number = 1

# Erstelle eine I2C-Verbindung
bus = smbus.SMBus(bus_number)

# Funktion zum Auslesen der Temperatur
def read_temperature():
    try:
        # Sende Anfrage an den Arduino, die Temperatur auszulesen
        bus.write_byte(arduino_address, 2)
        
        # Warte auf die Antwort des Arduino (0,1 Sekunden)
        time.sleep(0.1)
        
        # Lese die Antwort des Arduino (2 Bytes)
        temperature = bus.read_word_data(arduino_address, 0)
        
        # Konvertiere die Antwort in Grad Celsius
        temperature = temperature / 100.0
        
        return temperature
    
    except IOError as e:
        print("Fehler beim Kommunizieren mit dem Arduino: ", e)
        return None

def send_command(command):
    try:
        bus.write_byte(arduino_address, command)
        time.sleep(0.1)  # Pause, um die Kommunikation abzuschließen
        return True
    except IOError:
        return False

def turn_on_led():
    if send_command(1):
        print("LED eingeschaltet")
    else:
        print("Fehler beim Einschalten der LED")

def turn_off_led():
    if send_command(0):
        print("LED ausgeschaltet")
    else:
        print("Fehler beim Ausschalten der LED")

turn_on_led()
time.sleep(2)
turn_off_led()

# Endlosschleife für die Temperaturausgabe
while True:
    try:
        temperature = read_temperature()

        if temperature is not None:
            print("Temperatur: ", temperature, "°C")

        time.sleep(1)  # Warte 1 Sekunde zwischen den Auslesungen

    except KeyboardInterrupt:
        break
