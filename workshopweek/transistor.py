import RPi.GPIO as GPIO
import time

GPIO.setwarnings(False) 
GPIO.setmode(GPIO.BOARD)
GPIO.setup(7, GPIO.OUT)

try:
	while True:
		GPIO.output(7, True)
		time.sleep(1)
		GPIO.output(7, False)
		time.sleep(1)
except KeyboardInterrupt:
	pass

GPIO.cleanup()



