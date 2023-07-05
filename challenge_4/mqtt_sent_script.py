import paho.mqtt.client as mqtt
import time

mqtt_broker = "localhost"
mqtt_port = 1883
mqtt_usr = "admin"
mqtt_passw = "testing1234"
mqtt_water = "topic/water"
mqtt_gps = "topic/gps"
mqtt_display = "topic/display"
mqtt_availability = "topic/availability"
mqtt_next_ferry = "topic/next_ferry"

mqtt_availability_73 = "topic/availability/73"


def on_connect(client, userdata, flags, rc):
	print("Connected to MQTT broker: " + mqtt_broker)

def start_mqtt_client():
	client = mqtt.Client()
	client.username_pw_set(mqtt_usr, mqtt_passw)
	client.on_connect = on_connect
	client.connect(mqtt_broker, mqtt_port, 60)

	client.disconnect()

# Function to publish a message
def publish_message(topic, message):
	client = mqtt.Client()
	client.username_pw_set(mqtt_usr, mqtt_passw)
	client.connect(mqtt_broker, mqtt_port, 60)
	client.publish(topic, message)
	client.disconnect()
 
 
def main():
    start_mqtt_client()
    while True:
        publish_message(mqtt_availability_73, True)
        time.sleep(20)
        publish_message(mqtt_availability_73, False)
        time.sleep(20)
        
if __name__ == "__main__":
    main()