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

db_host = '104.211.25.177'
db_port = '6666'
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
# Array of speeds work with 5 levels, but not other count; trying to find function for that
v_speeds = [min_speed]
for i in range(num_levels):
	temperatures.append(temp_wanted + (i * level_difference))
	v_speeds.append(v_speeds[i]+(max_speed - min_speed)/(num_levels*2)*i)
temperatures.append(temperatures[num_levels-1] + level_difference)
v_speeds.pop(0)

v_speed_5 = 255
v_speed_4 = 210
v_speed_3 = 160
v_speed_2 = 130
v_speed_1 = 120

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
    		0: 0,
    		1: v_speed_1,
    		2: v_speed_2,
    		3: v_speed_3,
		    4: v_speed_4,
    		5: v_speed_5
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
	client.loop_forever()

# Function to publish a message
def publish_message(topic, message):
	client = mqtt.Client()
	client.username_pw_set(mqtt_usr, mqtt_passw)
	client.connect(mqtt_broker, mqtt_port, 60)
	client.publish(topic, message)
	client.disconnect()

def get_next_id(table):
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
    cursor.execute(f"INSERT INTO reading {formatted_columns} VALUES {data};")
    connection.commit()
    cursor.close()
    print('Inserted',data,'\nninto',table)
  
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
		manual_mode

		if manual_mode == True:
			print(f"Kühlung Stufe {manual_level}")
			vent_control(manual_vent)
			activate_leds(manual_level)

		elif manual_mode == False:
			temperature_thresholds = [
				(temperatures[5], 5, v_speed_5),
				(temperatures[4], 4, v_speed_4),
				(temperatures[3], 3, v_speed_3),
				(temperatures[2], 2, v_speed_2),
				(temperatures[1], 1, v_speed_1),
				(temperatures[0], 0, 0)
			]

			# Iterate over the temperature thresholds in reverse order
			for threshold, level, speed in temperature_thresholds:
				if not temp:
					continue  # Skip the current iteration if there is no value in temp
				if float(temp) >= threshold:
					print(f"Kühlung Stufe {level}")
					activate_leds(level)
					vent_control(speed)
					current_speed = speed
					break  # Exit the loop after the first match
				else:
					if not temp:
						print("No temperature value")
					else:
						continue
					activate_leds(0)
					vent_control(0)

		else:
			print("ERROR\nManual Mode holds:", manual_mode)

		# SQL Insertion for Temp
		if temp != temp_saved:
			reading_ID = db_get_next_pk_id("reading")

			# getting time
			current_time = datetime.now().strftime("%H:%M:%S")

			# adding new data
			cursor = connection.cursor()
			data_to_insert = (int(reading_ID), int(1), float(temp), str(current_time))
			insert_query = f"INSERT INTO reading VALUES (%s, %s, %s, %s)"
			cursor.execute(insert_query, data_to_insert)
			connection.commit()
			cursor.close()
			print('Temperature', temp, 'inserted into the table!')

			# This was indeed an event (adding event afterwards)
			event = True
   
			temp_saved = temp

		# SQL Insertion for Ventilation
		if vent != vent_saved:
			vent_stat_ID = db_get_next_pk_id("vent_stat")

			# getting time
			current_time = datetime.now().strftime("%H:%M:%S")

			# adding new data
			cursor = connection.cursor()
			data_to_insert = (int(vent_stat_ID), 1, int(vent) ,str(current_time))
			insert_query = f"INSERT INTO vent_stat VALUES (%s, %s, %s, %s)"
			cursor.execute(insert_query, data_to_insert)
			connection.commit()
			cursor.close()
			print('Ventilation', vent, 'inserted into the table!')

			# This was indeed an event (adding event afterwards)
			event = True

			vent_saved = vent

		if event:
			event_ID = db_get_next_pk_id("event")
			# getting time
			current_time = datetime.now().strftime("%H:%M:%S")

			# adding new data
			cursor = connection.cursor()
			data_to_insert = (int(event_ID),str(current_time),int(reading_ID),int(vent_stat_ID),float(temp))
			insert_query = f"INSERT INTO event VALUES (%s, %s, %s, %s, %s)"
			cursor.execute(insert_query, data_to_insert)
			connection.commit()
			cursor.close()
			print("Event inserted into the table!\n-----------------------------")

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
		print("PostgreSQL connection closed.")
	ser_led.close()
	ser_temp.close()
	ser_vent.close()
	print("closing arduinos and ending")
	time.sleep(1)
