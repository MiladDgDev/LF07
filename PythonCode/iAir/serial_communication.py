import time

import serial
import json


class ArduinoOfflineError(Exception):
    """Exception raised forArduino being offline."""

    def __init__(self,  message):
        self.message = message
        super().__init__(self.message)

    def __str__(self):
        return f"{self.message}"


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

    while is_active:
        try:
            ser.reset_input_buffer()  # Clears the input buffer
            ser.reset_output_buffer()  # Clears the output buffer

            ser.write(b'DATA')

            while ser.in_waiting > 0:
                response = ser.readline().decode('utf-8').rstrip()
                print(f"Received: {response}")

            data = ser.readline().decode('utf-8').strip()

            if data:
                print(f"Received: {data}")
                data_dict = json.loads(data)
                print(data_dict)
                return data_dict

            raise ArduinoOfflineError(message="Extracting data from the Arduino failed!")

        except KeyboardInterrupt:
            print("Exiting program...")
            is_active = False
            raise
        except ArduinoOfflineError as e:
            print(e.message)
            is_active = False
            raise
        finally:
            ser.close()


def write_to_serial_port(message: str) -> bool:

    is_active: bool = True

    ser = serial.Serial(
        port='/dev/ttyACM0',
        baudrate=115200,
        timeout=1
    )

    try:
        if ser.is_open:
            print(f"Connected to {ser.port}")
            ser.write(message.encode())
            ser.close()
            return True
        else:
            raise ArduinoOfflineError("Message didn't reach the Arduino!")
    except ArduinoOfflineError as e:
        print(e.message)
        raise
    except serial.SerialException as e:
        print(e)
        raise
    except Exception as e:
        print(e)
        raise
