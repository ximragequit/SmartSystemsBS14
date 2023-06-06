import smbus
import time
import struct

time.sleep(0.1)

# Adresse des Arduino
arduino_address_1 = 0x08
arduino_address_2 = 0x09

# I2C-Busnummer (normalerweise 1 auf dem Raspberry Pi)
bus_number = 1

# Erstelle eine I2C-Verbindung
bus = smbus.SMBus(bus_number)

# Funktion zum Auslesen der Temperatur
def read_temperature():
    try:
        # Sende Anfrage an den Arduino, die Temperatur auszulesen
        bus.write_byte(arduino_address_1, 2)
        
        # Warte auf die Antwort des Arduino (0,1 Sekunden)
        time.sleep(0.1)
        
        # Lese die Antwort des Arduino (2 Bytes)
        temperature = bus.read_word_data(arduino_address_1, 0)
        # Anfrage an den Arduino-Slave senden und Daten empfangen
        #temperature = bus.read_word_data(arduino_address, 0)
        #temperature = (((temperature & 0xFF) << 8) | ((temperature & 0xFF00) >> 8))
        # Konvertiere die Antwort in Grad Celsius
        #temperature = temperature / 100.0
        #temperature = temperature * 0.03675
        print("Temperatur:", (temperature / 100.0) * 0.0395, "°C")
        return (temperature / 100.0) * 0.0395
    
    except IOError as e:
        print("Fehler beim Kommunizieren mit dem Arduino: ", e)
        return None

def send_command(command):
    try:
        bus.write_byte(arduino_address_1, command)
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

i = 0
try:
    while i<30:
        #turn_on_led()
        #time.sleep(2)
        #turn_off_led()

        temperature = read_temperature()
        print(temperature)
        if temperature > 20:
            turn_on_led()
        else:
            turn_off_led()
        time.sleep(2)
        i += 1

except KeyboardInterrupt:
    pass


#bus.write_byte(arduino_address, 255)  # Annahme, dass 0xFF der Zurücksetzungsbefehl ist
turn_off_led()
temperature = 0
time.sleep(0.5)

bus.close()

time.sleep(0.1)
