
import serial

ser_temp = serial.Serial('/dev/ttyACM0', 9600)  # Arduino Temperatur

temp = ser_temp.readline().decode('utf-8').strip()

print(temp)

