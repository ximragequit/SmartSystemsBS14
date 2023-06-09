import serial
import time
import logging
import psycopg2
from datetime import datetime

# Configure logging
logging.basicConfig(filename='script.log', level=logging.ERROR, format='%(asctime)s - %(levelname)s - %(message)s')


try:
    # connect to Database
    connection = psycopg2.connect(
    host='192.168.4.84',
    database='postgres',
    user='postgres',
    password='testing1234'
    )
    print("Connected to the PostgreSQL database!")
	

        # getting highest ID
        cursor = connection.cursor()
        select_query = f"SELECT MAX(reading_id) FROM reading"
        cursor.execute(select_query)
        reading_ID_row = cursor.fetchone()
        print("reading_ID_row:", reading_ID_row)

                if reading_ID_row[0] is not None:
                        reading_ID = reading_ID_row[0] + 1
                else:
                        reading_ID = 1

                # reading_ID = (int(reading_ID_row[0]) + 1) if reading_ID_row and reading_ID_row[0] else 1
                print("reading_ID:", reading_ID)
                cursor.close()

                # getting time
                current_time = datetime.now().strftime("%H:%M:%S")

                temp = 20.00

                # adding new data
                cursor = connection.cursor()
                data_to_insert = (int(reading_ID), int(1), float(temp), str(current_time))
                print(int(reading_ID), int(1), float(temp), str(current_time))
                print(type(int(reading_ID)), type(int(1)), type(float(temp)), type(str(current_time)))
                insert_query = f"INSERT INTO reading VALUES (%s, %s, %s, %s)"
                cursor.execute(insert_query, (data_to_insert,))
                connection.commit()
                cursor.close()
                print("Data inserted into the table!") 


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
        time.sleep(1)
