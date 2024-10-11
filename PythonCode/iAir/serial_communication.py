import serial
import time

# Set up the serial connection
ser = serial.Serial(
    port='/dev/ttyACM0',        # Replace with your serial port name (e.g., '/dev/ttyUSB0' on Linux)
    baudrate=9600,      # Set the baud rate according to your device's specifications
    timeout=1           # Timeout in seconds for read operations
)

# Check if the serial port is open
if ser.is_open:
    print(f"Connected to {ser.port}")

# Read data from the serial port
try:
    while True:
        # Read a line (until a newline character) from the serial port
        data = ser.readline().decode('utf-8').strip()

        if data:
            print(f"Received: {data}")

except KeyboardInterrupt:
    print("Exiting program...")

# Close the serial connection
ser.close()

