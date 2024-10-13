import time

import serial
import json

import types_enums


class ArduinoOfflineError(Exception):
    """Exception raised forArduino being offline."""

    def __init__(self, message):
        self.message = message
        super().__init__(self.message)

    def __str__(self):
        return f"{self.message}"


def read_serial_port() -> types_enums.IndoorConditions:
    is_active: bool = True

    ser = serial.Serial(
        port='/dev/ttyACM0',
        baudrate=9600,
        timeout=1
    )

    try:
        if ser.is_open:
            print(f"Connected to Arduino! Waiting for the indoor conditions data!")
        else:
            raise ArduinoOfflineError("Arduino offline!")

        while is_active:

            data = ser.readline().decode('utf-8').strip()

            if data:
                data_dict = json.loads(data)
                for key in data_dict.keys():
                    print(f"{key}: {data_dict[key]}")
                print('\n')
                return data_dict

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
    ser = serial.Serial(
        port='/dev/ttyACM0',
        baudrate=9600,
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
