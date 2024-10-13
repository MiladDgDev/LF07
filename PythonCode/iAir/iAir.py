import datetime
import time
import repository
import types_enums
import serial_communication
import db_service
import weather_api_data

activity_has_started = False
activity_starting_time: datetime.datetime = datetime.datetime.now()


def process_data(data: types_enums.IndoorConditions):
    try:
        my_temperature = data["temperature"]

        my_humidity = data["humidity"]

        my_co2 = data["co2"]

        if my_temperature <= 14:
            repository.bad_indoor_condition['temperature_too_low'] = True
            repository.indoor_conditions = types_enums.Conditions.UNDESIRABLE
        if my_temperature >= 28:
            repository.bad_indoor_condition['temperature_too_high'] = True
            repository.indoor_conditions = types_enums.Conditions.UNDESIRABLE
        if my_humidity <= 30:
            repository.bad_indoor_condition["humidity_too_low"] = True
            repository.indoor_conditions = types_enums.Conditions.UNDESIRABLE
        if my_humidity >= 50:
            repository.bad_indoor_condition["humidity_too_high"] = True
            repository.indoor_conditions = types_enums.Conditions.UNDESIRABLE
        if my_co2 >= 850:
            repository.bad_indoor_condition["co2_too_high"] = True
            repository.indoor_conditions = types_enums.Conditions.UNDESIRABLE

        for key in repository.bad_indoor_condition.keys():
            if repository.bad_indoor_condition[key]:
                print(f"Issue: {key}")
            print('\n')

    except Exception as e:
        print(e)
        print("Analyzing the indoor conditions failed!")
        raise


def start_activity():
    print("OPEN THE WINDOWS!!!\n")


def stop_activity():
    print("CLOSE THE WINDOWS!!!\n")


def main():
    is_canceled: bool = False

    public_ip_tries: int = 0
    weather_api_tries: int = 0
    serial_communication_tries: int = 0

    while not is_canceled:
        try:
            # get outdoors weather data from the weather api
            weather_api_data.update_weather_repository()
            public_ip_tries = 0
            weather_api_tries = 0

            # get indoors conditions from the Arduino
            indoors_conditions: dict = serial_communication.read_serial_port()
            serial_communication_tries = 0

            # process the indoor conditions data from the Arduino
            process_data(indoors_conditions)

            # take action if necessary
            if repository.indoor_conditions is types_enums.Conditions.DESIRABLE:
                if activity_has_started:
                    stop_activity()
                    continue
                else:
                    continue
            else:
                if activity_has_started:
                    continue
                else:
                    start_activity()

        except KeyboardInterrupt as e:
            is_canceled = True
            print(e)

        except serial_communication.ArduinoOfflineError as ae:
            print(ae.message)
            if serial_communication_tries >= 4:
                print("Serial Communication with the Arduino failed for 5 consecutive Time. "
                      "Shutting program down. Please try again later.")
                is_canceled = True
                break
            print("Trying again in 5 seconds!")
            time.sleep(5)
            serial_communication_tries += 1
            continue

        except weather_api_data.PublicIpNotFound as pe:
            print(pe.message)
            if public_ip_tries >= 4:
                print("Public IP retrieval failed after 5 attempts. Shutting program down. Please try again later.")
                is_canceled = True
                break
            print("Trying again in 5 seconds!")
            time.sleep(5)
            public_ip_tries += 1
            continue

        except weather_api_data.WeatherApiOffline as we:
            print(we.message)
            if weather_api_tries >= 4:
                print("Weather API still offline after 5 attempts. Shutting program down. Please try again later.")
                is_canceled = True
                break
            print("Trying again in 5 seconds!")
            time.sleep(5)
            weather_api_tries += 1
            continue
            
        except Exception as e:
            print(e)
            is_canceled = True


main()
