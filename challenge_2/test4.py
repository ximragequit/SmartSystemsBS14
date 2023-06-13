import time
import random
import paho.mqtt.client as mqtt

# MQTT-Broker-Konfiguration
broker_address = "localhost"
broker_port = 1883
username = "admin"
password = "testing1234"

# Erstellen einer MQTT-Client-Instanz
client = mqtt.Client()

# Benutzerauthentifizierung festlegen
client.username_pw_set(username, password)

# Verbindung zum MQTT-Broker herstellen
client.connect(broker_address, broker_port)

# Zahlen von 20 bis 25 senden
for i in range(20, 26):
    # Zufällige Temperaturwert generieren
    temperature = random.uniform(20.0, 25.0)

    # Nachricht veröffentlichen
    client.publish("topic/temp", str(temperature))

    print(f"Temperaturwert {temperature} veröffentlicht")

    # Eine kurze Pause zwischen den Veröffentlichungen
    time.sleep(1)

# Verbindung zum MQTT-Broker beenden
client.disconnect()

