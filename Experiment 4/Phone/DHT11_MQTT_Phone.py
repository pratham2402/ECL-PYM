import paho.mqtt.client as mqtt
import Adafruit_DHT
import time

# Define the DHT11 sensor and GPIO pin
DHT_SENSOR = Adafruit_DHT.DHT11
DHT_PIN = 4  # GPIO 4

# MQTT Broker details (Raspberry Pi's IP)
MQTT_BROKER = ""  # Replace with your Raspberry Pi's IP
MQTT_PORT = 1883
MQTT_TOPIC = "test/topic"

# Create MQTT client and connect
client = mqtt.Client()
client.connect(MQTT_BROKER, MQTT_PORT, 60)

while True:
    # Read temperature and humidity
    humidity, temperature = Adafruit_DHT.read(DHT_SENSOR, DHT_PIN)

    if humidity is not None and temperature is not None:
        message = f"Temperature: {temperature:.1f}°C, Humidity: {humidity:.1f}%"
        print("Sending:", message)
        client.publish(MQTT_TOPIC, message)  # Publish to MQTT topic
    else:
        print("Failed to retrieve data from DHT11 sensor")

    time.sleep(5)  # Send data every 5 seconds
