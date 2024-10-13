import serial
import time

def read_serial_port() -> dict:
    is_active: bool = True

    ser = serial.Serial(
        port='/dev/ttyACM0',
        baudrate=9600,  # Match baud rate to Arduino
        timeout=1
    )

    time.sleep(2)

    if ser.is_open:
        print(f"Connected to {ser.port}")

        try:
            ser.write(b'DATA\n')  # Send DATA followed by a newline
            time.sleep(1)  # Wait for Arduino to process and respond

            data = ser.readline().decode('utf-8').strip()
            print(f"Received: {data}")

            ser.reset_input_buffer()  # Clears the input buffer
            ser.reset_output_buffer()  # Clears the output buffer

        except Exception as e:
            print(e)

        finally:
            ser.close()

read_serial_port()