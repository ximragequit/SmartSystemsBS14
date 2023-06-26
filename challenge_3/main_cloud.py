import serial
import time
import psycopg2
import logging
from datetime import datetime
import paho.mqtt.client as mqtt
import threading

# Configure logging
logging.basicConfig(
    filename='//Workshop/challenge_2/script.log', 
    level=logging.ERROR, 
    format='%(asctime)s - %(levelname)s - %(message)s'
)

ser_temp = serial.Serial('/dev/ttyACM0', 9600)  # Arduino Temperatur
ser_vent = serial.Serial('/dev/ttyACM1', 9600)  # Arduino Ventilator
ser_led = serial.Serial('/dev/ttyACM2', 9600)   # Arduino LED

mqtt_broker = "localhost"
mqtt_port = 1883
mqtt_usr = "admin"
mqtt_passw = "testing1234"
mqtt_temp = "topic/temp"
mqtt_level = "topic/level"
mqtt_setting = "topic/setting"

terminate_flag = threading.Event()

db_host = '104.211.25.177'
db_port = '5432'
db_database = 'icetruck'
db_usr = 'admin_hs'
db_pw = 'Testing1234'

temp_saved = 0.00
temp = 0.00
vent_saved = 0
vent = 0
duration = 300
start_time = time.time()
event = False
current_speed = 0

manual_mode = False
manual_level = 0
manual_vent = 0

global reading_ID
reading_ID = 1
global vent_stat_ID
vent_stat_ID = 1
global event_ID
event_ID = 1

temp_wanted = 25.00
num_levels = 5
level_difference = 0.20
max_speed = 255
min_speed = 120
temperatures = []
v_speeds = []

for i in range(num_levels):
	temperatures.append(temp_wanted + (i * level_difference))

	t = i / (num_levels - 1)  # Wertebereich von 0 bis 1
	x = t * t  # Quadratische Funktion
	wert = 120 + x * (255 - 120)  # Skalierung auf gewünschten Wertebereich
	v_speeds.append(round(wert))
temperatures.append(temperatures[num_levels-1] + level_difference)
v_speeds.insert(0,0)

def activate_leds(level):
	led_state = [1] * level + [0] * (5 - level)  # Create a list of LED states
	for led, state in enumerate(led_state, start=1):
		set_led_state(led, state)  # Set the state of each LED

def set_led_state(led, state):
	command = f'{led}{state}\n'
	ser_led.write(command.encode())

def vent_control(speed):
	global vent
	vent = speed
	# The str(int(str.. is somehow necessary
	ser_vent.write(str(int(str(vent))).encode()) # Wanted voltage for right speed
	time.sleep(1.5)

# Callback function for the on_connect event
def on_connect(client, userdata, flags, rc):
	print("Connected to MQTT broker: " + mqtt_broker)
	client.subscribe(mqtt_setting)
	client.subscribe(mqtt_level)

# Callback function for the on_message event
def on_message(client, userdata, msg):
	global manual_mode, manual_level, manual_vent
	print("Received message: " + str(msg.payload.decode()))
	if msg.topic == mqtt_setting:
		if (str(msg.payload.decode())) == 'True':
			manual_mode = True
			print("Manual Mode active")
			activate_leds(manual_level)
			vent_control(manual_vent)
		elif (str(msg.payload.decode())) == 'False':
			manual_mode = False
			print("Automatic Mode active")
			activate_leds(level)
			vent_control(current_speed)
		else:
			print(manual_mode)
	elif msg.topic == mqtt_level:
		manual_level = int(msg.payload.decode())
		vent_mapping = {
    		0: v_speeds[0],
    		1: v_speeds[1],
    		2: v_speeds[2],
    		3: v_speeds[3],
		    4: v_speeds[4],
    		5: v_speeds[5]
		}
		manual_vent = vent_mapping.get(manual_level)
		print("Recieved Level Value:", manual_level)

# Function to start the MQTT client
def start_mqtt_client():
	client = mqtt.Client()
	client.username_pw_set(mqtt_usr, mqtt_passw)
	client.on_connect = on_connect
	client.on_message = on_message
	client.connect(mqtt_broker, mqtt_port, 60)
 
	while not terminate_flag.is_set():
		client.loop()
		time.sleep(0.1)
	
	client.disconnect()

# Function to publish a message
def publish_message(topic, message):
	client = mqtt.Client()
	client.username_pw_set(mqtt_usr, mqtt_passw)
	client.connect(mqtt_broker, mqtt_port, 60)
	client.publish(topic, message)
	client.disconnect()

def db_get_next_pk_id(table):
    cursor = connection.cursor()
    table_id = table + "_id"
    select_query = f"SELECT MAX({table_id}) FROM {table}"
    cursor.execute(select_query)
    table_id_row = cursor.fetchone()
    cursor.close()
    if table_id_row[0] is not None:
        return(table_id_row[0] + 1)
    else:
	    return 1
 
# not implemented yet, just prepared
def db_insert_data(table, data):
    cursor = connection.cursor()
    cursor.execute(f"SELECT * FROM {table} LIMIT 0")
    colnames = [desc[0] for desc in cursor.description]
    formatted_columns = '(' + ', '.join(colnames) + ')'
    cursor.close()
    
    # Needs a check if data has same amount of Contents as there are Columns in this table
    cursor = connection.cursor()
    cursor.execute(f"INSERT INTO {table} {formatted_columns} VALUES {data};")
    connection.commit()
    cursor.close()
    print('Inserted',data,'into',table, formatted_columns)
  
try:
	# connect to Database
	connection = psycopg2.connect(
	host = db_host,
	port = db_port,
	database = db_database,
	user = db_usr,
	password = db_pw
	)
	print("Connected to the PostgreSQL database!")

	# Start the MQTT client in a separate thread
	mqtt_thread = threading.Thread(target=start_mqtt_client)
	mqtt_thread.start()

	while True:
		temp = ser_temp.readline().decode('utf-8').strip()

		message_temp = str(temp)
		publish_message(mqtt_temp, message_temp)

		if manual_mode == True:
			print(f"Kühlung Stufe {manual_level}")
			vent_control(manual_vent)
			activate_leds(manual_level)

		elif manual_mode == False:
			temperature_thresholds = [
				(temperatures[5], 5, v_speeds[5]),
				(temperatures[4], 4, v_speeds[4]),
				(temperatures[3], 3, v_speeds[3]),
				(temperatures[2], 2, v_speeds[2]),
				(temperatures[1], 1, v_speeds[1]),
				(temperatures[0], 0, v_speeds[0])
			]

			# Iterate over the temperature thresholds in reverse order
			for threshold, level, speed in temperature_thresholds:
				if not temp or float(temp) < 0:
					continue  # Skip the current iteration if there is no value in temp
				elif float(temp) >= threshold:
					print(f"Kühlung Stufe {level}")
					activate_leds(level)
					vent_control(speed)
					current_speed = speed
					break  # Exit the loop after the first match

		else:
			print("ERROR\nManual Mode holds:", manual_mode)

		# SQL Insertion for Temp
		if temp != temp_saved:
			reading_ID = db_get_next_pk_id("reading")

			# getting time
			current_time = datetime.now().strftime("%H:%M:%S")

			# adding new data
			data = (int(reading_ID), int(1), float(temp), str(current_time))
			db_insert_data('reading', data)

			# This was indeed an event (adding event afterwards)
			event = True
   
			temp_saved = temp

		# SQL Insertion for Ventilation
		if vent != vent_saved:
			vent_stat_ID = db_get_next_pk_id("vent_stat")

			# getting time
			current_time = datetime.now().strftime("%H:%M:%S")

			# adding new data
			data = (int(vent_stat_ID), 1, int(vent) ,str(current_time))
			db_insert_data('vent_stat', data)

			# This was indeed an event (adding event afterwards)
			event = True

			vent_saved = vent

		if event:
			event_ID = db_get_next_pk_id("event")
			# getting time
			current_time = datetime.now().strftime("%H:%M:%S")

			# adding new data
			data = (int(event_ID),str(current_time),int(reading_ID),int(vent_stat_ID),float(temp))
			db_insert_data('event', data)
			print("____________________________")

			# need to check again next time
			event = False

		if time.time() - start_time >= duration:
			print("That was long enough")
			break

except serial.SerialException as se:
	logging.error(f"Serial communication error: {se}")
	print(f"Serial communication error: {se}")
except psycopg2.Error as pe:
	logging.error(f"PostgreSQL database error: {pe}")
	print(f"PostgreSQL database error: {pe}")
except psycopg2.errors.SyntaxError as se:
	logging.error(f"PostgreSQL syntax error: {se}")
	print(f"PostgreSQL syntax error: {se}")
except KeyboardInterrupt:
	logging.info("KeyboardInterrupt: Script interrupted by user")
	print("KeyboardInterrupt: Script interrupted by user")
except Exception as e:
	logging.exception(f"An unexpected error occurred: {e}")
	print(f"An unexpected error occurred: {e}")

finally:
	# Close the database connection
	if connection:
		connection.close()
		print("__________________________\nPostgreSQL connection closed.")
	activate_leds(0)
	vent_control(0)
	time.sleep(0.5)
	ser_led.close()
	ser_temp.close()
	ser_vent.close()
	print("__________________________\nArduino connection closed.")
	terminate_flag.set()
	mqtt_thread.join()
	print("__________________________\nMQTT client terminated.")
	time.sleep(1)