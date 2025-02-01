import BlynkLib
import RPi.GPIO as GPIO

# Blynk Auth Token (Replace with your own token)
BLYNK_AUTH = ''

# Initialize Blynk
blynk = BlynkLib.Blynk(BLYNK_AUTH, server="blynk.cloud")

# Define GPIO pin for LED
LED_PIN = 4 

# Set up GPIO
GPIO.setmode(GPIO.BCM)
GPIO.setup(LED_PIN, GPIO.OUT)
GPIO.output(LED_PIN, GPIO.LOW)  # Start with LED off

# Function to control LED via Virtual Pin V2
@blynk.on("V2")
def control_led(value):
    if int(value[0]) == 1:
        GPIO.output(LED_PIN, GPIO.HIGH)  # Turn LED ON
        print("LED ON")
    else:
        GPIO.output(LED_PIN, GPIO.LOW)   # Turn LED OFF
        print("LED OFF")

# Main loop
while True:
    blynk.run()

