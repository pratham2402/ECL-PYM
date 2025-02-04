import Adafruit_DHT
import paho.mqtt.client as mqtt
import time

# Set the sensor type and GPIO pin number
DHT_SENSOR = Adafruit_DHT.DHT11
DHT_PIN = 4  # GPIO pin where the sensor is connected

# MQTT broker details
MQTT_BROKER = ""  # Replace with your Ubuntu laptop's IP address
MQTT_PORT = 1883
MQTT_TOPIC = "home/temperature_humidity"

# Create MQTT client
client = mqtt.Client()
client.connect(MQTT_BROKER, MQTT_PORT, 60)

while True:
    # Read the sensor data
    humidity, temperature = Adafruit_DHT.read(DHT_SENSOR, DHT_PIN)
    
    if humidity is not None and temperature is not None:
        # Print the values on the console
        print(f"Temperature={temperature}C  Humidity={humidity}%")
        
        # Publish the data to the MQTT broker
        message = f"Temperature={temperature}C, Humidity={humidity}%"
        client.publish(MQTT_TOPIC, message)
    else:
        print("Failed to retrieve data from sensor.")
    
    # Wait for 10 seconds before reading again
    time.sleep(2)
