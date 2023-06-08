import serial
import time

ser_0 = serial.Serial('/dev/ttyACM0', 9600)  # Arduino Temperatur
ser_1 = serial.Serial('/dev/ttyACM1', 9600)  # Arduino Ventilator

max = 26
temp_saved = 0.00
temp = 0.00
runtime = True
start_time = time.time()

def vent_control(command):
    ser_1.write(command.encode())

while runtime:
    time_actual = time.time()
    if time_actual - start_time >= 300:
        runtime = False
    else:
        print(time_actual - start_time)
    temp = ser_0.readline().decode('utf-8').strip()
    if temp:
        print(float(temp))
        if float(temp) >= 24:
            print("Ventilator an")
            vent_control('1')
        elif float(temp) < 5:
            print("error")
        elif float(temp) < 24:
            print("Ventilator aus")
            vent_control('0')
        else:
            print("das darfst du nicht lesen")
    
