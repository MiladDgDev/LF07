import asyncio
import requests
import repository


class WeatherApiOffline(Exception):
    """Exception raised for Weather API being offline."""

    def __init__(self, message):
        self.message = message
        super().__init__(self.message)

    def __str__(self):
        return f"{self.message}"


class PublicIpNotFound(Exception):
    """Exception raised for Public IP Retrieval Failure."""

    def __init__(self, message):
        self.message = message
        super().__init__(self.message)

    def __str__(self):
        return f"{self.message}"


def get_public_ip() -> str:
    try:
        response = requests.get('https://api.ipify.org/?format=json')

        if response.status_code != 200:
            raise PublicIpNotFound(f"Public IP retrieval failed: code {response.status_code}")
        
        return response.json()['ip']

    except PublicIpNotFound as pe:
        print(pe.message)
        raise
    except Exception:
        raise


def get_weather_data(public_ip: str) -> dict:
    api_root = "https://api.weatherapi.com/v1/"
    api_key = "868342ede06a4f5eadd85825240210"

    ip_address = public_ip

    try:
        response = requests.get(f"{api_root}current.json?key={api_key}&q={ip_address}&aqi=no")
        data = response.json()

        if response.status_code != 200:
            http_response_code = response.status_code
            error_code = data['code']
            message = data['message']
            raise WeatherApiOffline(message=f'Weather Data Retrieval Failed! '
                                            f'\nHTTP Response Code: {http_response_code}'
                                            f'\nError Code: {error_code}'
                                            f'\nMessage: {message}')

        current_fetched_values = data['current']
        temperature = current_fetched_values['temp_c']
        is_day = current_fetched_values['is_day']
        condition = current_fetched_values['condition']['text']
        humidity = current_fetched_values['humidity']

        current_condition = {
            "temperature": temperature,
            "is_day": is_day,
            "condition": condition,
            "humidity": humidity
        }

        return current_condition

    except WeatherApiOffline as we:
        print(we.message)
        raise
    except Exception as ex:
        print(ex.args)
        raise


def update_weather_repository() -> None:
    my_ip: str = ''

    try:
        my_ip = get_public_ip()
    except Exception as e:
        print(e.args)
        raise

    if my_ip != '':
        print(f"My Public IP: {my_ip}")
        try:
            weather_data = get_weather_data(my_ip)

            repository.regional_temperature = weather_data['temperature']
            repository.regional_humidity = weather_data['humidity']

            if weather_data['is_day'] == 1:
                repository.is_day = True
            else:
                repository.is_day = False

            repository.regional_weather_condition = weather_data['condition']

            print(f'Weather data successfully updated:\n'
                  f'regional temperature: {repository.regional_temperature}\n'
                  f'regional humidity: {repository.regional_humidity}\n'
                  f'regional conditions: {repository.regional_weather_condition}\n'
                  f'Daytime: {repository.is_day}')

        except Exception as ex:
            print(ex.args)
            raise
