import smbus
import time

# Adresse des Arduino auf dem I2C-Bus
arduino_address = 0x08

# I2C-Bus-Instanz erstellen
bus = smbus.SMBus(1)

def set_led_state(state):
    bus.write_byte_data(arduino_address, 0, state)

def set_fan_state(state):
    bus.write_byte_data(arduino_address, 1, state)

def read_temperature():
    raw_value = bus.read_word_data(arduino_address, 2)
    # Der Arduino sendet den Temperaturwert als 16-Bit-Wort (2 Bytes) zurück
    # Hier musst du die Logik anpassen, um den Temperaturwert in Grad Celsius zu berechnen
    # Dies hängt von deinem spezifischen Temperatursensor ab.
    temperature = raw_value / 100.0  # Beispiel: Annahme, dass der Wert als Ganzzahl mit 2 Dezimalstellen gesendet wird
    return temperature

try:
    while True:
        temperature = read_temperature()
        print("Temperatur: {:.2f}°C".format(temperature))

        if temperature > 22:
            set_led_state(1)  # LED einschalten
            set_fan_state(1)  # Ventilator einschalten
        else:
            set_led_state(0)  # LED ausschalten
            set_fan_state(0)  # Ventilator ausschalten

        time.sleep(1)

except KeyboardInterrupt:
    set_led_state(0)  # LED ausschalten
    set_fan_state(0)  # Ventilator ausschalten
