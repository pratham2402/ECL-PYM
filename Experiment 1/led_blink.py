import RPi.GPIO as GPIO
import time

# Pin configuration
LED_PIN = 18  # GPIO pin where the LED is connected

# GPIO setup
GPIO.setmode(GPIO.BCM)  # Use BCM pin numbering
GPIO.setup(LED_PIN, GPIO.OUT)

try:
    while True:
        GPIO.output(LED_PIN, GPIO.HIGH)  # Turn LED on
        print("LED is ON")
        time.sleep(1)  # Keep LED on for 1 second

        GPIO.output(LED_PIN, GPIO.LOW)   # Turn LED off
        print("LED is OFF")
        time.sleep(1)  # Keep LED off for 1 second

except KeyboardInterrupt:
    print("\nExiting program...")

finally:
    GPIO.cleanup()  # Reset GPIO settings
    print("GPIO cleaned up.")

