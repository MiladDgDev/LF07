import serial_communication


def serial_write():
    try:
        success = serial_communication.write_to_serial_port("Hello Milad\n")
        if success:
            print("message sent!")
        else:
            print("message not sent")
    except Exception as e:
        print(e)


serial_communication.read_serial_port();