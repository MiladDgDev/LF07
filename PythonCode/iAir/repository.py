import types_enums

regional_temperature: float = -100

regional_humidity: float = 0

is_day: bool = True

regional_weather_condition: str = ''

indoor_conditions: types_enums.Conditions = types_enums.Conditions.DESIRABLE

bad_indoor_condition: types_enums.BadIndoorCondition = dict(temperature_too_high=False,
                                                            temperature_too_low=False,
                                                            humidity_too_high=False,
                                                            humidity_too_low=False,
                                                            co2_too_high=False)

