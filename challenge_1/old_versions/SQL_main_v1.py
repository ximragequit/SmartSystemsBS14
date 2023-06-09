import serial
import time
import psycopg2

ser_temp = serial.Serial('/dev/ttyACM0', 9600)  # Arduino Temperatur
ser_vent = serial.Serial('/dev/ttyACM1', 9600)  # Arduino Ventilator
ser_led = serial.Serial('/dev/ttyACM2', 9600)   # Arduino LED

temp_saved = 0.00
temp = 0.00
vent_saved = 0
vent = 0
duration = 300
start_time = time.time()
event = False

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

def led_on(led):
        command = f'{led}{1}\n'
        ser_led.write(command.encode())

def led_off(led):
        command = f'{led}{0}\n'
        ser_led.write(command.encode())


def activate_leds(level):
        if level == 0:
                led_off(1)
                led_off(2)
                led_off(3)
                led_off(4)
                led_off(5)
        elif level == 1:
                led_on(1)
                led_off(2)
                led_off(3)
                led_off(4)
                led_off(5)
        elif level == 2:
                led_on(1)
                led_on(2)
                led_off(3)
                led_off(4)
                led_off(5)
        elif level == 3:
                led_on(1)
                led_on(2)
                led_on(3)
                led_off(4)
                led_off(5)
        elif level == 4:
                led_on(1)
                led_on(2)
                led_on(3)
                led_on(4)
                led_off(5)
        elif level == 5:
                led_on(1)
                led_on(2)
                led_on(3)
                led_on(4)
                led_on(5)

def vent_control(speed):
        global vent
        vent = speed
        # ignore the str(int(str.. because this shit idk
        ser_vent.write(str(int(str(vent))).encode()) # Wanted voltage for right speed
        print(vent)
        time.sleep(1.5)


try:
        # connect to Database
        connection = psycopg2.connect(
        host='192.168.4.181',
        database='postgres',
        user='postgres',
        password='testing1234'
        )
        print("Connected to the PostgreSQL database!")


        while True:
                temp = ser_temp.readline().decode('utf-8').strip()
                if not temp:
                        continue
                print(float(temp))
                if float(temp) >= temp_5:
                        print("Kühlung Stufe 5")
                        activate_leds(5)
                        vent_control(v_speed_5)
                elif float(temp) >= temp_4:
                        print("Kühlung Stufe 4")
                        activate_leds(4)
                        vent_control(v_speed_4)
                elif float(temp) >= temp_3:
                        print("Kühlung Stufe 3")
                        activate_leds(3)
                        vent_control(v_speed_3)
                elif float(temp) >= temp_2:
                        print("Kühlung Stufe 2")
                        activate_leds(2)
                        vent_control(v_speed_2)
                elif float(temp) >= temp_1:
                        print("Kühlung Stufe 1")
                        activate_leds(1)
                        vent_control(v_speed_1)
                elif float(temp) <= temp_wanted:
                        print("Kühl genug")
                        activate_leds(0)
                        vent_control(0)

                # SQL Insertion for Temp
                if temp != temp_saved:
                        # getting highest ID
                        cursor = connection.cursor()
                        select_query = f"SELECT MAX(reading_id) FROM reading"
                        cursor.execute(select_query)
                        reading_ID = ((cursor.fetchone())[0] + 1)
                        cursor.close()

                        # adding new data
                        cursor = connection.cursor()
                        data_to_insert = (reading_ID,'1',temp,time)
                        insert_query = f"INSERT INTO reading VALUES (%s, %s, %s, %s)"
                        cursor.execute(insert_query, (data_to_insert,))
                        connection.commit()
                        cursor.close()
                        print("Data inserted into the table!") 

                        # This was indeed an event (adding event afterwards)
                        event = True

                # SQL Insertion for Ventilation
                if vent != vent_saved:
                        # getting highest ID
                        cursor = connection.cursor()
                        select_query = f"SELECT MAX(vent_stat_id) FROM vent_stats"
                        cursor.execute(select_query)
                        vent_stat_ID = ((cursor.fetchone())[0] + 1)
                        cursor.close()

                        # adding new data
                        cursor = connection.cursor()
                        data_to_insert = (vent_stat_ID,'1',vent,time)
                        insert_query = f"INSERT INTO vent_stats VALUES (%s, %s, %s, %s)"
                        cursor.execute(insert_query, (data_to_insert,))
                        connection.commit()
                        cursor.close()
                        print("Data inserted into the table!")

                        # This was indeed an event (adding event afterwards)
                        event = True
                
                if event:
                        # getting highest ID
                        cursor = connection.cursor()
                        select_query = f"SELECT MAX(event_id) FROM events"
                        cursor.execute(select_query)
                        event_ID = ((cursor.fetchone())[0] + 1)
                        cursor.close()   

                        # adding new data
                        cursor = connection.cursor()
                        data_to_insert = (event_ID,time,reading_ID,vent_stat_ID,temp)
                        insert_query = f"INSERT INTO events VALUES (%s, %s, %s, %s, %s)"
                        cursor.execute(insert_query, (data_to_insert,))
                        connection.commit()
                        cursor.close()
                        print("Data inserted into the table!")

                        # need to check again next time
                        event = False

                if time.time() - start_time >= duration:
                        print("That was long enough")
                        break

except psycopg2.Error as e:
                print(f"Error connecting to the PostgreSQL database: {e}")

except KeyboardInterrupt as x:
        print(f"KeyboardInterrupt: {x}")

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
