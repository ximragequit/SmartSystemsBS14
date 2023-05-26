import RPi.GPIO as GPIO
import time

GPIO.setwarnings(False)  # Warnmeldungen deaktivieren

GPIO.setmode(GPIO.BCM)
GPIO.setup(3, GPIO.OUT)

pwm = GPIO.PWM(3, 1000)
pwm.start(0)

def update_fan_speed():
    pot_value = GPIO.input(2)
    duty_cycle = pot_value * 100 / 1023
    pwm.ChangeDutyCycle(duty_cycle)
    print("running...")

GPIO.setup(2, GPIO.IN, pull_up_down=GPIO.PUD_UP)

try:
    while True:
        update_fan_speed()
        time.sleep(0.1)  # Eine kurze Pause von 0.1 Sekunden
except KeyboardInterrupt:
    pwm.stop()
    GPIO.cleanup()
