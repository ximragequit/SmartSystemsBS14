import logging, time, datetime
import psycopg2
import time
import serial

logging.basicConfig(
    format = '______________________\n%(levelname)-2s %(asctime)s \n%(message)s',
    filename = F'.\challenge_4\Prototyping\logs\{datetime.today().strftime("%y.%m.%d")}_py.log', 
    encoding = 'utf-8', 
    level = logging.DEBUG,
    datefmt='%y.%m.%d %H:%M:%S'
    )

ser_display = serial.Serial('/dev/ttyACM0', 9600)  # Port und Baudrate anpassen
ser_water = serial.Serial('/dev/ttyACM1', 9600)  # Port und Baudrate anpassen

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

def main():
    # main code
    clear_display()
    move_cursor(0, 0)
    write_text("Hello, World!")
    water = ser_water.readline().decode('utf-8').strip()
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
        #cleanup
        pass