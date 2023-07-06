import serial
import time
import psycopg2
import logging
from datetime import datetime
import paho.mqtt.client as mqtt

logging.basicConfig(
	format = '______________________\n%(levelname)-2s %(asctime)s \n%(message)s',
	filename = F'.\challenge_4\Prototyping\logs\{datetime.today().strftime("%y.%m.%d")}_py.log', 
	encoding = 'utf-8', 
	level = logging.DEBUG,
	datefmt='%y.%m.%d %H:%M:%S'
	)

ser_display = serial.Serial('/dev/ttyACM0', 9600)  # Port und Baudrate anpassen
ser_water = serial.Serial('/dev/ttyACM1', 9600)  # Port und Baudrate anpassen
# useless comment

mqtt_broker = "localhost"
mqtt_port = 1883
mqtt_usr = "admin"
mqtt_passw = "testing1234"
mqtt_water = "topic/water"
mqtt_gps = "topic/gps"
mqtt_display = "topic/display"
mqtt_availability = "topic/availability"
mqtt_availability_73 = "topic/availability/73"
mqtt_next_ferry = "topic/next_ferry/73"

db_host = 'localhost'
db_port = '5432'
db_database = 'postgres'
db_usr = 'postgres'
db_pw = 'testing1234'

display_message = "HADAG raus!"
actual_coordinates = "your mum"
ferry_availability = True
max_water_level = 275

# Callback function for the on_connect event
def on_connect(client, userdata, flags, rc):
	print("Connected to MQTT broker: " + mqtt_broker)

# Function to start the MQTT client
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

def clear_display():
	ser_display.write(b'C')

def move_cursor(column, row):
	ser_display.write(b'M')
	ser_display.write(str(column).encode())
	ser_display.write(b' ')
	ser_display.write(str(row).encode())

def write_text(text):
	ser_display.write(b'W')
	ser_display.write(text.encode())
	ser_display.write(b'\n')

def get_db():
	return psycopg2.connect(
			   host = db_host,
			   port = db_port,
			   database = db_database,
			   user = db_usr,
			   password = db_pw
			   )

def db_get_next_pk_id(table):
	db = get_db()
	cursor = db.cursor()
	table_id = table + "_id"
	select_query = f"SELECT MAX({table_id}) FROM {table}"
	cursor.execute(select_query)
	table_id_row = cursor.fetchone()
	cursor.close()
	db.close()
	if table_id_row[0] is not None:
		return(table_id_row[0] + 1)
	else:
		return 1

def db_insert_data(table, data):

	db = get_db()
	print("Connected to the PostgreSQL database!")
	cursor = db.cursor()

	cursor.execute(f"SELECT * FROM {table} LIMIT 0")
	colnames = [desc[0] for desc in cursor.description]
	formatted_columns = '(' + ', '.join(colnames) + ')'
	cursor.close()

	# Needs a check if data has same amount of Contents as there are Columns in this table
	cursor = db.cursor()
	cursor.execute(f"INSERT INTO {table} {formatted_columns} VALUES {data};")
	db.commit()
	cursor.close()
	print('Inserted',data,'into',table, formatted_columns)

	db.close()

def get_minutes(ferryLine_ID,dock_ID):
    db = get_db()
    cursor = db.cursor()

    # SQL-Abfrage ausführen
    cursor.execute(
        """
        SELECT DepartureTime
        FROM Schedule
        WHERE FerryLine_ID = {ferryLine_ID}
        AND Dock_ID = {dock_ID}
        ORDER BY DepartureTime
        """
    )

    # Ergebnisse abrufen
    results = cursor.fetchall()

    # Liste der Abfahrtszeiten erstellen
    departure_times = [row[0] for row in results]

    current_time = datetime.now().time()

    # Nächstgrößere Abfahrtszeit finden
    next_departure_time = None
    for departure_time in departure_times:
        if departure_time > current_time:
            next_departure_time = departure_time
            break

    cursor.close()
    db.close()
    # Berechnung der Differenz in Minuten
    if next_departure_time is not None:
        # Aktuelles Datum und Uhrzeit mit der nächsten Abfahrtszeit kombinieren
        current_datetime = datetime.combine(datetime.now().date(), current_time)
        next_departure_datetime = datetime.combine(datetime.now().date(), next_departure_time)

        # Differenz berechnen
        time_difference = next_departure_datetime - current_datetime

        # Differenz in Minuten extrahieren
        time_difference_minutes = time_difference.total_seconds() // 60
    return time_difference_minutes

def clear_display():
    ser_display.write(b'C')

def move_cursor(column, row):
    ser_display.write(b'M')
    ser_display.write(str(column).encode())
    ser_display.write(b' ')
    ser_display.write(str(row).encode())

def write_text(text):
    ser_display.write(b'W')
    ser_display.write(text.encode())
    ser_display.write(b'\n')

def mqtt_publish_left_minutes():
    publish_message(mqtt_next_ferry+"/Landungsbrücken","Landungsbrücken:"+get_minutes(6,1))
    publish_message(mqtt_next_ferry+"/Theater im Hafen","Theater im Hafen:"+get_minutes(6,14))
    publish_message(mqtt_next_ferry+"/Argentinienbrücke","Argentinienbrücke:"+get_minutes(6,15))
    publish_message(mqtt_next_ferry+"/Ernst-August-Schleuse","Ernst-August-Schleuse:"+get_minutes(6,16))

def main():
	# main code
	# connect to Database

	start_mqtt_client()
	while True:
		time.sleep(0.5)
		clear_display()
		# datetime object containing current date and time
		now = datetime.now().strftime("%y.%m.%d;%H:%M:%S")

		print("now =", now)

		# get waterlevel and publish
		water_ID = db_get_next_pk_id("WaterLevel")
		water = ser_water.readline().decode('utf-8').strip()
		water_data = (int(water_ID), str(now), float(water))
		db_insert_data('WaterLevel',water_data)
		print(water)
		#message_water = str(water)
		#publish_message(mqtt_water, message_water)

		minutes_left = int(get_minutes(6,16))

		mqtt_publish_left_minutes()

		if int(water) < max_water_level: #ferry is available
			ferry_availability = True
		else:
			ferry_availability = False

		publish_message(mqtt_availability_73, ferry_availability)

		if ferry_availability:
			time.sleep(0.25)
			move_cursor(0, 0)
			time.sleep(0.25)
			write_text("Faehre faehrt in") # depending on schedule from database
			time.sleep(0.25)
			move_cursor(0, 1)
			time.sleep(0.25)
			write_text(str(minutes_left) + " Minuten.")
			time.sleep(0.25)
		else:
			time.sleep(0.25)
			move_cursor(0, 0)
			time.sleep(0.25)
			write_text("Faehre fahrt")
			time.sleep(0.25)
			move_cursor(0, 1)
			time.sleep(0.25)
			write_text("momentan nicht!")
			time.sleep(0.25)

	pass



if __name__ == "__main__":
	try:
		main()
	
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
		clear_display()
		time.sleep(0.5)
		ser_water.close()
		ser_display.close()
		print("__________________________\nArduino connection closed.")
		print("__________________________\nMQTT client terminated.")
		time.sleep(1)
		pass