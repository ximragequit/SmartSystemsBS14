import RPi.GPIO as GPIO
import time

# Pin numbers
motor_pin = 5
potentiometer_pin = 3

# GPIO setup
GPIO.setmode(GPIO.BOARD)
GPIO.setup(motor_pin, GPIO.OUT)
GPIO.setup(potentiometer_pin, GPIO.IN)

# Create PWM object for motor control
pwm = GPIO.PWM(motor_pin, 100)  # Frequency of PWM signal (100 Hz)

# Start PWM with initial duty cycle
initial_duty_cycle = 0
pwm.start(initial_duty_cycle)

# Main loop
try:
    while True:
        # Read analog value from potentiometer
        pot_value = GPIO.input(potentiometer_pin)
        
        # Map the analog value to the duty cycle range (0-100)
        duty_cycle = int(pot_value / 1023 * 100)
        
        # Update the motor speed
        pwm.ChangeDutyCycle(duty_cycle)
        
        # Delay for stability (adjust as needed)
        time.sleep(0.1)

except KeyboardInterrupt:
    pass

# Clean up GPIO
pwm.stop()
GPIO.cleanup()
