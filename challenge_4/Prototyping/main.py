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

def main():
    # main code
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