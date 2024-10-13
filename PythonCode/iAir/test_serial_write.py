import serial_communication
import serial
import time


def read_serial_port() -> dict:
    is_active: bool = True

    ser = serial.Serial(
        port='/dev/ttyACM0',
        baudrate=115200,
        timeout=1
    )

    time.sleep(2)

    if ser.is_open:
        print(f"Connected to {ser.port}")

        try:
            ser.reset_input_buffer()  # Clears the input buffer
            ser.reset_output_buffer()  # Clears the output buffer

            ser.write(b'DATA')
            time.sleep(1)
            while ser.in_waiting > 0:
                data = ser.readline().decode('utf-8').strip()
                print(f"Received: {data}")

        except Exception as e:
            print(e.message)

        finally:
            ser.close()


read_serial_port()
