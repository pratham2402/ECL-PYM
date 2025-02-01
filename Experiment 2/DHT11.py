import Adafruit_DHT
import time

# Sensor configuration
DHT_SENSOR = Adafruit_DHT.DHT11
DHT_PIN = 4  # GPIO pin where the DHT11 sensor is connected

try:
    while True:
        humidity, temperature = Adafruit_DHT.read(DHT_SENSOR, DHT_PIN)  # Read sensor data
        if humidity is not None and temperature is not None:
            print(f"Temp: {temperature:.1f}°C  Humidity: {humidity:.1f}%")
        else:
            print("Failed to retrieve data from humidity sensor")
        time.sleep(2)  # Wait 2 seconds before the next read

except KeyboardInterrupt:
    print("\nExiting program...")

finally:
    print("Program terminated.")
