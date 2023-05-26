from pyfirmata import Arduino, util
import time

# Ultraschallsensor Pins
trigPin = 2
echoPin = 3

# Verbindung zum Arduino herstellen
board = Arduino('/dev/ttyACM0')  # Serieller Anschluss des Arduinos (angepasst an deine Konfiguration)

# Initialisierung des Ultraschallsensors
trig = board.get_pin('d:{}:o'.format(trigPin))
echo = board.get_pin('d:{}:i'.format(echoPin))

def setup():
    # Nichts zu initialisieren
    pass

def get_distance():
    # Senden des Ultraschallimpulses
    trig.write(0)
    time.sleep(0.2)
    trig.write(1)
    time.sleep(0.00001)
    trig.write(0)

    # Messen der Dauer des Echo-Signals
    pulse_start = time.time()
    while echo.read() == 0:
        if time.time() - pulse_start > 2:  # Timeout von 2 Sekunden, falls kein Echo empfangen wird
            return None
    pulse_end = time.time()
    pulse_duration = pulse_end - pulse_start

    # Berechnung der Entfernung basierend auf der Schallgeschwindigkeit
    speed_of_sound = 34300  # Schallgeschwindigkeit in cm/s
    distance = pulse_duration * speed_of_sound / 2

    return distance

def main():
    setup()
    it = util.Iterator(board)
    it.start()
    try:
        while True:
            distance = get_distance()
            if distance is not None:
                print("Entfernung: {:.2f} cm".format(distance))
            else:
                print("Fehler: Timeout beim Messen der Entfernung")
            time.sleep(1)
    except KeyboardInterrupt:
        pass

if __name__ == '__main__':
    main()
