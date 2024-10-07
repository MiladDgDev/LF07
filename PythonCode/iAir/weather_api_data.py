import asyncio
import requests


async def get_public_ip() -> str:
    try:
        response = requests.get('https://api.ipify.org/?format=json')

        if response.status_code != 200:
            raise Exception('IP Address Retrieval Failed!')

        return response.json()['ip']
    except Exception as e:
        raise e

async def get_weather_data(public_ip: str) -> dict:
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
            raise Exception(f'Weather Data Retrieval Failed! '
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

    except Exception as ex:
        print(ex.args)


async def print_weather() -> None:
    my_ip: str = ''

    try:
        my_ip = await get_public_ip()
    except Exception as e:
        print(e.args)

    if my_ip != '':
        print(f"My Public IP: {my_ip}")
        try:
            weather_data = await get_weather_data(my_ip)
            print(weather_data)
        except Exception as ex:
            print(ex.args)

asyncio.run( print_weather())
