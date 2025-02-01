from flask import Flask, render_template, jsonify
import Adafruit_DHT

# Flask app setup
app = Flask(__name__)

# Sensor configuration
DHT_SENSOR = Adafruit_DHT.DHT11
DHT_PIN = 17  # GPIO pin where the DHT11 sensor is connected

def get_sensor_data():
    humidity, temperature = Adafruit_DHT.read(DHT_SENSOR, DHT_PIN)  # Read sensor data
    if humidity is not None and temperature is not None:
        return {'temperature': temperature, 'humidity': humidity}
    else:
        return {'temperature': None, 'humidity': None}

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/sensor-data')
def sensor_data():
    data = get_sensor_data()
    return jsonify(data)  # Return data as JSON

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
