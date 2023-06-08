import smbus
import time

# I2C-Adresse des Arduino
arduino_address = 0x08

# Initialisierung des I2C-Bus
bus = smbus.SMBus(1)  # Je nach Raspberry Pi-Modell kann die Nummerierung variieren (0 oder 1)

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

# Beispielanwendung
turn_on_led()
time.sleep(2)
turn_off_led()
