import datetime
import time
import repository
import types_enums
import serial_communication
import db_service
import weather_api_data

activity_has_started: bool = False
activity_starting_time: datetime.datetime = datetime.datetime.now()

weather_api_fetch_successful: bool = False
last_weather_api_fetch_time: datetime.datetime = datetime.datetime.now() - datetime.timedelta(minutes=11)


def process_data(data: types_enums.IndoorConditions):
    try:
        my_temperature = data["temperature"]

        my_humidity = data["humidity"]

        my_co2 = data["co2"]

        if my_temperature <= 14:
            repository.bad_indoor_condition['temperature_too_low'] = True
            repository.indoor_conditions = types_enums.Conditions.UNDESIRABLE
        elif my_temperature >= 28:
            repository.bad_indoor_condition['temperature_too_high'] = True
            repository.indoor_conditions = types_enums.Conditions.UNDESIRABLE
        else:
            repository.bad_indoor_condition['temperature_too_low'] = False
            repository.bad_indoor_condition['temperature_too_high'] = False
            repository.indoor_conditions = types_enums.Conditions.DESIRABLE

        if my_humidity <= 30:
            repository.bad_indoor_condition["humidity_too_low"] = True
            repository.indoor_conditions = types_enums.Conditions.UNDESIRABLE
        elif my_humidity >= 50:
            repository.bad_indoor_condition["humidity_too_high"] = True
            repository.indoor_conditions = types_enums.Conditions.UNDESIRABLE
        else:
            repository.bad_indoor_condition["humidity_too_high"] = False
            repository.bad_indoor_condition["humidity_too_low"] = False
            repository.indoor_conditions = types_enums.Conditions.DESIRABLE

        if my_co2 >= 850:
            repository.bad_indoor_condition["co2_too_high"] = True
            repository.indoor_conditions = types_enums.Conditions.UNDESIRABLE
        else:
            repository.bad_indoor_condition["co2_too_high"] = False
            repository.indoor_conditions = types_enums.Conditions.DESIRABLE

        if repository.indoor_conditions == types_enums.Conditions.UNDESIRABLE:
            print(f"Indoor conditions: Undesirable!\n")
        else:
            print(f"Indoor conditions: Desirable!\n")

        for key in repository.bad_indoor_condition.keys():
            if repository.bad_indoor_condition[key]:
                print(f"Issue: {key}")

        print('\n')

    except Exception as e:
        print(e)
        print("Analyzing the indoor conditions failed!")
        raise


def start_activity(indoor_conditions: types_enums.IndoorConditions):
    global activity_has_started

    if repository.bad_indoor_condition['humidity_too_high']:
        if indoor_conditions['humidity'] > repository.regional_humidity:
            print("OPEN THE WINDOWS!!!\n\n")
            if not activity_has_started:
                activity_has_started = True
                success = db_service.add_activity(repository.indoor_conditions,
                                                  indoor_conditions['temperature'],
                                                  indoor_conditions['humidity'],
                                                  indoor_conditions['co2'],
                                                  types_enums.Commands.OPEN)
                if success:
                    print("\nStarting the activity was successfully logged to the database!")
        else:
            print("Situation outdoors is worse! Opening the windows won't be helpful!\n"
                  f"Outdoors Humidity: {repository.regional_humidity}")

    if repository.bad_indoor_condition['humidity_too_low']:
        if indoor_conditions['humidity'] < repository.regional_humidity:
            print("OPEN THE WINDOWS!!!\n\n")
            if not activity_has_started:
                activity_has_started = True
                success = db_service.add_activity(repository.indoor_conditions,
                                                  indoor_conditions['temperature'],
                                                  indoor_conditions['humidity'],
                                                  indoor_conditions['co2'],
                                                  types_enums.Commands.OPEN)
                if success:
                    print("\nStarting the activity was successfully logged to the database!")
        else:
            print("Situation outdoors is worse! Opening the windows won't be helpful!\n"
                  f"Outdoors Humidity: {repository.regional_humidity}")

    if repository.bad_indoor_condition['temperature_too_high']:
        if indoor_conditions['temperature'] > repository.regional_temperature:
            print("OPEN THE WINDOWS!!!\n\n")
            if not activity_has_started:
                activity_has_started = True
                success = db_service.add_activity(repository.indoor_conditions,
                                                  indoor_conditions['temperature'],
                                                  indoor_conditions['humidity'],
                                                  indoor_conditions['co2'],
                                                  types_enums.Commands.OPEN)
                if success:
                    print("\nStarting the activity was successfully logged to the database!")
        else:
            print("Situation outdoors is worse! Opening the windows won't be helpful!\n"
                  f"Outdoors Temperature: {repository.regional_temperature}")

    if repository.bad_indoor_condition['temperature_too_low']:
        if indoor_conditions['temperature'] < repository.regional_temperature:
            print("OPEN THE WINDOWS!!!\n\n")
            if not activity_has_started:
                activity_has_started = True
                success = db_service.add_activity(repository.indoor_conditions,
                                                  indoor_conditions['temperature'],
                                                  indoor_conditions['humidity'],
                                                  indoor_conditions['co2'],
                                                  types_enums.Commands.OPEN)
                if success:
                    print("\nStarting the activity was successfully logged to the database!")
        else:
            print("Situation outdoors is worse! Opening the windows won't be helpful!\n"
                  f"Outdoors Temperature: {repository.regional_temperature}")

    if repository.bad_indoor_condition['co2_too_high']:
        print("OPEN THE WINDOWS!!!\n\n")
        if not activity_has_started:
            activity_has_started = True
            success = db_service.add_activity(repository.indoor_conditions,
                                              indoor_conditions['temperature'],
                                              indoor_conditions['humidity'],
                                              indoor_conditions['co2'],
                                              types_enums.Commands.OPEN)
            if success:
                print("\nStarting the activity was successfully logged to the database!")


def stop_activity(indoor_conditions: types_enums.IndoorConditions):
    global activity_has_started
    print("CLOSE THE WINDOWS!!!\n\n")
    if activity_has_started:
        success = db_service.add_activity(repository.indoor_conditions,
                                          indoor_conditions['temperature'],
                                          indoor_conditions['humidity'],
                                          indoor_conditions['co2'],
                                          types_enums.Commands.CLOSE)
        if success:
            activity_has_started = False
            print("\nStopping the activity was successfully logged to the database!")


def main():
    global activity_has_started
    global last_weather_api_fetch_time
    is_canceled: bool = False

    public_ip_tries: int = 0
    weather_api_tries: int = 0
    serial_communication_tries: int = 0

    while not is_canceled:
        try:
            # get outdoors weather data from the weather api
            if weather_api_fetch_successful:
                if (last_weather_api_fetch_time - datetime.datetime.now()).total_seconds() > 60 * 10:
                    weather_api_data.update_weather_repository()
                    public_ip_tries = 0
                    weather_api_tries = 0
                    last_weather_api_fetch_time = datetime.datetime.now()
            else:
                weather_api_data.update_weather_repository()
                public_ip_tries = 0
                weather_api_tries = 0
                last_weather_api_fetch_time = datetime.datetime.now()

            # get indoors conditions from the Arduino
            indoors_conditions: dict = serial_communication.read_serial_port()
            serial_communication_tries = 0

            # process the indoor conditions data from the Arduino
            process_data(indoors_conditions)

            # take action if necessary
            if repository.indoor_conditions is types_enums.Conditions.DESIRABLE:
                if activity_has_started:
                    stop_activity(indoors_conditions)
                    continue
                else:
                    continue
            else:
                if activity_has_started:
                    continue
                else:
                    start_activity(indoors_conditions)

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
