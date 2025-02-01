import RPi.GPIO as GPIO
import time

# Pin configuration
LED_PIN = 18  # GPIO pin where the LED is connected
BUTTON_PIN = 17  # GPIO pin where the button is connected

# GPIO setup
GPIO.setmode(GPIO.BCM)  # Use BCM pin numbering
GPIO.setup(LED_PIN, GPIO.OUT)  # Set LED pin as output
GPIO.setup(BUTTON_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)  # Set button pin as input with pull-up resistor

try:
    while True:
        button_state = GPIO.input(BUTTON_PIN)  # Read the button state
        if button_state == GPIO.LOW:  # Button pressed
            GPIO.output(LED_PIN, GPIO.LOW)  # Turn LED on
            print("LED is OFF")
        else:
            GPIO.output(LED_PIN, GPIO.HIGH)  # Turn LED off
            print("LED is ON")
        time.sleep(0.1)  # Small delay to debounce the button

except KeyboardInterrupt:
    print("\nExiting program...")

finally:
    GPIO.cleanup()  # Reset GPIO settings
    print("GPIO cleaned up.")
