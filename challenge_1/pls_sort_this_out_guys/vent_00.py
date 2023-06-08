import serial

ser_1 = serial.Serial('/dev/ttyACM1', 9600)  # Port anpassen, falls erforderlich

while True:
    speed = int(input("Geschwindigkeit des Ventilators (0-255): "))
    ser_1.write(str(speed).encode())
