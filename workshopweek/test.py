import pyfirmata
import time

board = pyfirmata.Arduino('/dev/ttyACM0')

echo = board.digital[5]
anaecho = board.analog[5]
trig = board.digital[6]


echo.mode = pyfirmata.INPUT
anaecho.mode = pyfirmata.INPUT
anaecho.enable_reporting()

it = pyfirmata.util.Iterator(board)
it.start()

def distance():
	trig.write(1)

	time.sleep(0.00001)
	trig.write(0)

	StartZeit = time.time()
	StopZeit = time.time()

	output = echo.read()
	value = anaecho.read()
	print(value)
	return output


#		GPIO.input(GPIO_ECHO) == 0:
#        	StartZeit = time.time()

#	while GPIO.input(GPIO_ECHO) == 1:
 #       	StopZeit = time.time()

  #  	TimeElapsed = StopZeit - StartZeit
#	distanz = (TimeElapsed * 34300) / 2
#	return distanz

if __name__ == '__main__':
	try:
		while True:
			distValue = distance()
			print (distValue)
			time.sleep(1)

	except KeyboardInterrupt:
		print("stop")
		exit()
