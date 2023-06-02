import smbus
import time

time.sleep(0.1)

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
        temperature = temperature * 0.03675
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


i = 0

while i<3:
    turn_on_led()
    time.sleep(2)
    turn_off_led()
    
    temperature = read_temperature()
    print(temperature)
    
    time.sleep(0.5)
    i += 1


#bus.write_byte(arduino_address, 255)  # Annahme, dass 0xFF der Zurücksetzungsbefehl ist

time.sleep(0.5)

bus.close()

time.sleep(0.1)
