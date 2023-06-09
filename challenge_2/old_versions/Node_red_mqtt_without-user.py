import serial
import time
import psycopg2
import logging
from datetime import datetime
import paho.mqtt.client as mqtt
import threading

# Configure logging
logging.basicConfig(filename='script.log', level=logging.ERROR, format='%(asctime)s - %(levelname)s - %(message)s')

ser_temp = serial.Serial('/dev/ttyACM0', 9600)  # Arduino Temperatur
ser_vent = serial.Serial('/dev/ttyACM1', 9600)  # Arduino Ventilator
ser_led = serial.Serial('/dev/ttyACM2', 9600)   # Arduino LED

mqtt_broker = "localhost"
mqtt_port = 1883
mqtt_temp = "topic/temp"
mqtt_level = "topic/level"
mqtt_setting = "topic/setting"

temp_saved = 0.00
temp = 0.00
vent_saved = 0
vent = 0
duration = 300
start_time = time.time()
event = False

manual_mode = False

global reading_ID
reading_ID = 1
global vent_stat_ID
vent_stat_ID = 1
global event_ID
event_ID = 1

temp_5 = 26.00
temp_4 = 25.80
temp_3 = 25.60
temp_2 = 25.40
temp_1 = 25.20
temp_wanted = 25.00

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

# Callback function for the on_message event
def on_message(client, userdata, msg):
    print("Received message: " + str(msg.payload.decode()))
    if bool(msg.payload.decode()) != manual_mode:
        global manual_mode
        manual_mode = bool(msg.payload.decode())
        print("Manual Mode active" if manual_mode else "Automatic Mode active")

# Function to start the MQTT client
def start_mqtt_client():
    client = mqtt.Client()
    client.on_connect = on_connect
    client.on_message = on_message
    client.connect(mqtt_broker, mqtt_port, 60)
    client.loop_forever()

# Function to publish a message
def publish_message(topic, message):
    client = mqtt.Client()
    client.connect(mqtt_broker, mqtt_port, 60)
    client.publish(topic, message)
    client.disconnect()

try:
    # connect to Database
    connection = psycopg2.connect(
    host='localhost',
    database='postgres',
    user='postgres',
    password='testing1234'
    )
    print("Connected to the PostgreSQL database!")

    # Start the MQTT client in a separate thread
    mqtt_thread = threading.Thread(target=start_mqtt_client)
    mqtt_thread.start()

    while True:
        temp = ser_temp.readline().decode('utf-8').strip()

        message_temp = str(temp)
        publish_message(mqtt_temp, message_temp)

        if manual_mode:
            print("here")
        else:
            temperature_thresholds = [
                (temp_5, 5, v_speed_5),
                (temp_4, 4, v_speed_4),
                (temp_3, 3, v_speed_3),
                (temp_2, 2, v_speed_2),
                (temp_1, 1, v_speed_1),
                (temp_wanted, 0, 0)
            ]

            # Iterate over the temperature thresholds in reverse order
            for threshold, level, speed in temperature_thresholds:
                if not temp:
                    continue  # Skip the current iteration if there is no value in temp
                if float(temp) >= threshold:
                    print(f"Kühlung Stufe {level}")
                    activate_leds(level)
                    vent_control(speed)
                    break  # Exit the loop after the first match
                else:
                    if not temp:
                            print("No temperature value")
                    else:
                            print("Kühl genug")
                    activate_leds(0)
                    vent_control(0)

            # SQL Insertion for Temp
            if temp != temp_saved:
                    # getting highest ID
                    cursor = connection.cursor()
                    select_query = f"SELECT MAX(reading_id) FROM reading"
                    cursor.execute(select_query)
                    reading_ID_row = cursor.fetchone()
                    if reading_ID_row[0] is not None:
                            reading_ID = reading_ID_row[0] + 1
                    else:
                            reading_ID = 1
                    cursor.close()

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

           # SQL Insertion for Ventilation
           if vent != vent_saved:
                # getting highest ID
                cursor = connection.cursor()
                select_query = f"SELECT MAX(vent_stat_id) FROM vent_stats"
                cursor.execute(select_query)
                vent_stat_ID_row = cursor.fetchone()
                if vent_stat_ID_row[0] is not None:
                        vent_stat_ID = vent_stat_ID_row[0] + 1
                else:
                        vent_stat_ID = 1
                cursor.close()

                # getting time
                current_time = datetime.now().strftime("%H:%M:%S")

                # adding new data
                cursor = connection.cursor()
                data_to_insert = (int(vent_stat_ID), 1, int(vent) ,str(current_time))
                insert_query = f"INSERT INTO vent_stats VALUES (%s, %s, %s, %s)"
                cursor.execute(insert_query, data_to_insert)
                connection.commit()
                cursor.close()
                print('Ventilation', vent, 'inserted into the table!')

                # This was indeed an event (adding event afterwards)
                event = True

        if event:
                # getting highest ID
                cursor = connection.cursor()
                select_query = f"SELECT MAX(event_id) FROM events"
                cursor.execute(select_query)
                event_ID_row = cursor.fetchone()
                if event_ID_row[0] is not None:
                        event_ID = event_ID_row[0] + 1
                else:
                        event_ID = 1
                cursor.close()

                # getting time
                current_time = datetime.now().strftime("%H:%M:%S")

                # adding new data
                cursor = connection.cursor()
                data_to_insert = (int(event_ID),str(current_time),int(reading_ID),int(vent_stat_ID),float(temp))
                insert_query = f"INSERT INTO events VALUES (%s, %s, %s, %s, %s)"
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
