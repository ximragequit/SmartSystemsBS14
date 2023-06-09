import paho.mqtt.client as mqtt

# Callback-Funktion, die aufgerufen wird, wenn eine Verbindung zum MQTT-Broker hergestellt wurde
def on_connect(client, userdata, flags, rc):
    print("Verbunden mit MQTT-Broker. Rückgabewert: " + str(rc))
    # Hier können Sie weitere Aktionen ausführen, wenn die Verbindung hergestellt wurde

# Callback-Funktion, die aufgerufen wird, wenn eine MQTT-Nachricht empfangen wird
def on_message(client, userdata, msg):
    print("Neue MQTT-Nachricht erhalten. Thema: " + msg.topic + "  Nachricht: " + str(msg.payload))
    # Hier können Sie die empfangenen Nachrichten verarbeiten


 # Verbindung zum MQTT-Broker herstellen
    client = mqtt.Client()
    client.on_connect = on_connect
    client.on_message = on_message

    client.connect("192.168.4.129", 1883, 60)

    # Unendliche Schleife, um auf eingehende MQTT-Nachrichten zu warten
    client.loop_forever()

    topic = "Haus/Dachboden/Licht"  # Das gewünschte MQTT-Thema angeben
    message = "Hallo, dies ist eine MQTT-Nachricht!"  # Die gewünschte Nachricht angeben
    client.publish(topic, message)
