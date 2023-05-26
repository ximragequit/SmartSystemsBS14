import RPi.GPIO as GPIO
import time

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.setup(3, GPIO.OUT)

def update_speaker_volume():
    GPIO.setup(26, GPIO.OUT)  # GPIO 26 als Ausgang setzen
    GPIO.output(26, GPIO.LOW)  # GPIO 26 auf niedrigen Zustand setzen
    time.sleep(0.1)  # Kurze Pause zum Entladen des Kondensators

    GPIO.setup(26, GPIO.IN)  # GPIO 26 als Eingang setzen
    start_time = time.time()

    while GPIO.input(26) == GPIO.LOW:
        pass

    end_time = time.time()
    charging_time = end_time - start_time

    # Berechnung des analogen Werts basierend auf der Ladezeit
    analog_value = int(charging_time * 1000)
    print("Analog Value:", analog_value)

    # Hier kannst du den analogen Wert in eine Aktion umwandeln, z. B. die Lautstärke des Lautsprechers setzen

GPIO.setup(26, GPIO.IN, pull_up_down=GPIO.PUD_UP)  # GPIO 26 als Eingang mit Pull-Up-Widerstand

try:
    while True:
        update_speaker_volume()
        time.sleep(1)

except KeyboardInterrupt:
    GPIO.cleanup()
