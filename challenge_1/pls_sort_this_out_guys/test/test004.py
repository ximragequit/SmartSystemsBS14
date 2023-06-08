import smbus
import struct
import time

# I2C-Adresse des Arduino
arduino_address = 0x08

# Initialisierung des I2C-Bus
bus = smbus.SMBus(1)

def read_temperature():
    # Befehl an den Arduino senden, um die Temperatur zu lesen
    bus.write_byte(arduino_address, ord('t'))
    
    # Kurze Verzögerung, um dem Arduino Zeit zu geben, die Temperatur zu messen
    time.sleep(0.1)
    
    # Daten vom Arduino lesen
    data = bus.read_i2c_block_data(arduino_address, 0, 4)
    
    # Temperatur aus den empfangenen Daten extrahieren
    temperature = struct.unpack('f', bytearray(data))[0]
    
    return temperature

def main():
    while True:
        # Temperatur lesen
        temperature = read_temperature()
        
        # Temperatur anzeigen
        print("Gemessene Temperatur:", temperature, "Grad Celsius")
        
        # Überprüfen, ob die Temperatur 22 Grad Celsius überschreitet
        if temperature > 22:
            # Befehl an den Arduino senden, um die Lampe und den Ventilator einzuschalten
            bus.write_byte(arduino_address, ord('o'))
        else:
            # Befehl an den Arduino senden, um die Lampe und den Ventilator auszuschalten
            bus.write_byte(arduino_address, ord('f'))
        
        # Kurze Verzögerung zwischen den Messungen
        time.sleep(1)

if __name__ == '__main__':
    main()
