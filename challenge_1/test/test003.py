import smbus

arduino_address = 0x08

def set_led_state(state):
    bus = smbus.SMBus(1)
    bus.write_byte_data(arduino_address, 0, state)

def read_temperature():
    bus = smbus.SMBus(1)
    temperature = bus.read_byte(arduino_address)
    return temperature

# Hauptprogramm
if __name__ == '__main__':
    temperature = read_temperature()
    print(f'Temperatur: {temperature} °C')

    if temperature > 22:
        set_led_state(1)  # LED einschalten
        print('LED eingeschaltet')
    else:
        set_led_state(0)  # LED ausschalten
        print('LED ausgeschaltet')
