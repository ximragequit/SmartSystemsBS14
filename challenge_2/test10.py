import paho.mqtt.client as mqtt

# Verbindungsinformationen für den MQTT-Broker
mqtt_broker = "localhost"
mqtt_port = 1883
mqtt_topic = "topic/test"  # Das gewünschte MQTT-Thema

mqtt_topic = "topic/temp"


# Callback-Funktion für das on_connect-Ereignis
def on_connect(client, userdata, flags, rc):
    print("Verbunden mit dem MQTT-Broker: " + mqtt_broker)
    client.publish("topic/temp", "Hallo von Python!")
    print("Published: " + "")

# MQTT-Client erstellen und mit dem Broker verbinden
client = mqtt.Client()
client.on_connect = on_connect
client.connect(mqtt_broker, mqtt_port, 60)

# Auf eingehende MQTT-Nachrichten warten
client.loop_forever()

