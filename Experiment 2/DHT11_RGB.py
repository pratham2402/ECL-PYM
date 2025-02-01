import smbus
import time
import Adafruit_DHT

# Define the I2C address of the LCD
LCD_ADDRESS = 0x3E
RGB_ADDRESS = 0x62

DHT_SENSOR = Adafruit_DHT.DHT11
# DHT11 sensor pin
DHT_PIN = 17  # Change this to the GPIO pin you're using

# Initialize the I2C bus
bus = smbus.SMBus(1)

def send_command(cmd):
    """Send a command to the LCD."""
    bus.write_byte_data(LCD_ADDRESS, 0x80, cmd)

def send_data(data):
    """Send data to the LCD."""
    bus.write_byte_data(LCD_ADDRESS, 0x40, data)

def set_rgb(r, g, b):
    """Set the backlight color of the LCD."""
    bus.write_byte_data(RGB_ADDRESS, 0x00, 0x00)
    bus.write_byte_data(RGB_ADDRESS, 0x01, 0x00)
    bus.write_byte_data(RGB_ADDRESS, 0x08, 0xAA)
    bus.write_byte_data(RGB_ADDRESS, 0x04, r)
    bus.write_byte_data(RGB_ADDRESS, 0x03, g)
    bus.write_byte_data(RGB_ADDRESS, 0x02, b)

def initialize_lcd():
    """Initialize the LCD."""
    send_command(0x01)  # Clear display
    time.sleep(0.05)
    send_command(0x38)  # Function set: 8-bit, 2 lines
    send_command(0x0C)  # Display ON, Cursor OFF, Blink OFF
    send_command(0x06)  # Entry mode set: increment, no shift
    time.sleep(0.05)

def write_message(line1, line2):
    """Write a message to the LCD."""
    send_command(0x80)  # Move cursor to the beginning of the first line
    for char in line1:
        send_data(ord(char))
    send_command(0xC0)  # Move cursor to the beginning of the second line
    for char in line2:
        send_data(ord(char))

def get_humidity():
    """Get the humidity from the DHT11 sensor."""
    humidity, _ = Adafruit_DHT.read(DHT_SENSOR, DHT_PIN)
    return humidity

if __name__ == "__main__":
    try:
        initialize_lcd()

        while True:
            humidity = get_humidity()

            if humidity is not None:
                write_message(f"Humidity: {humidity}%", "")
                
                # Check the humidity and set RGB color
                if humidity > 36:
                    set_rgb(255, 0, 0)  # Red
                elif humidity < 36:
                    set_rgb(0, 0, 255)  # Blue
                else:
                    set_rgb(0, 255, 0)  # Green
            else:
                write_message("", "")
                set_rgb(255, 0, 0)  # Red for error

            time.sleep(2)  # Refresh every 2 seconds

    except KeyboardInterrupt:
        send_command(0x01)  # Clear display
        set_rgb(0, 0, 0)  # Turn off backlight
        print("Exiting...")

