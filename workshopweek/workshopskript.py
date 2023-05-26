import pyfirmata
import time

board = pyfirmata.Arduino('/dev/ttyACM0')

US_TRIG = board.digital[6]
US_ECHO = board.digital[5]

US_ECHO.mode = pyfirmata.INPUT
US_ECHO.enable_reporting()

it = pyfirmata.util.Iterator(board)
it.start()

while True:
	US_TRIG.write(1)
	time.sleep(0.00001)
	US_TRIG.write(0)
	motion_state = US_ECHO.read()
	time.sleep(2)
	print(motion_state)
