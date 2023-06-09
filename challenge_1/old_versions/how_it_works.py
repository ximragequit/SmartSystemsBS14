import serial

ser = serial.Serial('/dev/ttyACM0', 9600)  # Port anpassen, falls erforderlich

while True:
    line = ser.readline().decode('utf-8').strip()
    if line:
        print(line)
