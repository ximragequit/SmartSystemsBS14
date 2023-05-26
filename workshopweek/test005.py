import RPi.GPIO as GPIO
import time

GPIO.setwarnings(False)  # Warnmeldungen deaktivieren

GPIO.setmode(GPIO.BCM)
GPIO.setup(3, GPIO.OUT)

pwm = GPIO.PWM(3, 1000)
pwm.start(0)

def update_fan_speed():
    GPIO.output(3, GPIO.HIGH)  # Ventilator einschalten
    print("running...")
    # Führe weitere Aufgaben oder Code aus...

try:
    while True:
        update_fan_speed()
        time.sleep(1)  # Eine kurze Pause von 0.1 Sekunden
except KeyboardInterrupt:
    pwm.stop()
    GPIO.cleanup()

