import RPi.GPIO as GPIO
import time

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.setup(3, GPIO.OUT)

pwm = GPIO.PWM(3, 1000)
pwm.start(0)

def update_buzzer_volume():
    pot_value = GPIO.input(26)
    duty_cycle = pot_value * 100 / 1023
    pwm.ChangeDutyCycle(duty_cycle)
    print(duty_cycle)

GPIO.setup(26, GPIO.IN, pull_up_down=GPIO.PUD_UP)  # Initialisierung des Potentiometer-Eingangs

try:
    while True:
        update_buzzer_volume()
        time.sleep(0.3)  # Eine kurze Pause von 0.1 Sekunden

except KeyboardInterrupt:
    pwm.stop()
    GPIO.cleanup()
