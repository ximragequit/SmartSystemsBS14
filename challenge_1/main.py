import serial
import time

ser_temp = serial.Serial('/dev/ttyACM0', 9600)  # Arduino Temperatur
ser_vent = serial.Serial('/dev/ttyACM1', 9600)  # Arduino Ventilator
ser_led = serial.Serial('/dev/ttyACM2', 9600)   # Arduino LED

max = 26
temp_saved = 0.00
temp = 0.00
runtime = True
duration = 300
start_time = time.time()


temp_5 = 26.00
temp_4 = 25.80
temp_3 = 25.60
temp_2 = 25.40
temp_1 = 25.20

v_speed_5 = 255
v_speed_4 = 210
v_speed_3 = 160
v_speed_2 = 130
v_speed_1 = 120

def led_on(led):
	command = f'{led}{1}\n'
	ser_led.write(command.encode())

def led_off(led):
	command = f'{led}{0}\n'
	ser_led.write(command.encode())


def activate_leds(level):
	if level == 0:
		led_off(1)
		led_off(2)
		led_off(3)
		led_off(4)
		led_off(5)
	elif level == 1:
		led_on(1)
		led_off(2)
		led_off(3)
		led_off(4)
		led_off(5)
	elif level == 2:
		led_on(1)
		led_on(2)
		led_off(3)
		led_off(4)
		led_off(5)
	elif level == 3:
		led_on(1)
		led_on(2)
		led_on(3)
		led_off(4)
		led_off(5)
	elif level == 4:
		led_on(1)
		led_on(2)
		led_on(3)
		led_on(4)
		led_off(5)
	elif level == 5:
		led_on(1)
		led_on(2)
		led_on(3)
		led_on(4)
		led_on(5)

def vent_control(speed):
	# ignore the str(int(str.. because this shit idk
	ser_vent.write(str(int(str(speed))).encode()) # Wanted voltage for right speed
	print(speed)
	time.sleep(1.5)


while runtime:
	# only run for [duration] seconds
	if time.time() - start_time >= duration:
		runtime = False
	else:
		print(time.time() - start_time)
		temp = ser_temp.readline().decode('utf-8').strip()
		if temp:
			print(float(temp))
			if float(temp) >= temp_5:
				print("Ventilator Stufe 5")
				activate_leds(5)
				vent_control(v_speed_5)
			elif float(temp) >= temp_4:
				print("Vent Stufe 4")
				activate_leds(4)
				vent_control(v_speed_4)
			elif float(temp) >= 25.60:
				print("Ventilator Stufe 3")
				activate_leds(3)
				vent_control(v_speed_3)
			elif float(temp) >= 25.40:
				print("Ventilator Stufe 2")
				activate_leds(2)
				vent_control(v_speed_2)
			elif float(temp) >= 25.20:
				print("Ventilator Stufe 1")
				activate_leds(1)
				vent_control(v_speed_1)
			elif float(temp) <= 25:
				print("Ventilator aus")
				activate_leds(0)
				vent_control(0)
