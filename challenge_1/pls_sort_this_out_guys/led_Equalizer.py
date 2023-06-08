import serial
import time

ser_temp = serial.Serial('/dev/ttyACM0', 9600)  # Port anpassen, falls erforderlich
ser_led = serial.Serial('/dev/ttyACM1', 9600)

time.sleep(2)

def set_led_state(led, state):
    command = f'{led}{state}\n'  # Befehl für den Arduino (z.B. "15" für LED an Pin 15)
    ser.write(command.encode())  # Sendet den Befehl an den Arduino


while True:
    line = ser.readline().decode('utf-8').strip()
    ledpin1 = 1
    ledpin2 = 5
    ledpin3 = 4
    ledpin4 = 3
    ledpin5 = 2


    if line:
        print(line)
    if line > 25
