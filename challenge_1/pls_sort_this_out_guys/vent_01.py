import serial
import time

ser = serial.Serial('/dev/ttyACM1', 9600)  # Port anpassen, falls erforderlich

def set_fan_speed(speed):
    ser.write(str(speed).encode())
    time.sleep(1)  # Wartezeit, um sicherzustellen, dass der Befehl gesendet wird

# Beispiel: Ventilator mit Geschwindigkeit 150 ansteuern

while True:
    set_fan_speed(150)
