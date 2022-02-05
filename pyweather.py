# main, pyweather.py

import argparse
import json
import pycountry
import style
import sys
import time

from configparser import ConfigParser
from datetime import datetime
from pprint import pp
from urllib import error, parse, request

# TODO: Add an arrow for wind direction... if 20 > deg > 60 NW arrow,
# if 60 > deg > 120 W arrow... or make dynamic arrow?

WEATHER_API_URL = "https://api.openweathermap.org/data/2.5/weather"

# Weather Condition Codes
# https://openweathermap.org/weather-conditions#Weather-Condition-Codes-2
THUNDERSTORM = range(200, 300)
DRIZZLE = range(300, 400)
RAIN = range(500, 600)
SNOW = range(600, 700)
ATMOSPHERE = range(700, 800)
CLEAR = range(800, 801)
CLOUDY = range(801, 900)



def weather_query_builder(city_input, metric=False):
    api_key = _get_api_key()
    city_name = " ".join(city_input)
    url_encoded_city_name = parse.quote_plus(city_name)
    units = "metric" if metric else "imperial"
    url = (
        f"{WEATHER_API_URL}?q={url_encoded_city_name}"
        f"&units={units}&appid={api_key}"
    )
    return url

def get_weather_data(query_url):
    try:
        response = request.urlopen(query_url)
    except error.HTTPError as http_error:
        if http_error.code == 401: 
            sys.exit("Access denied. Please check your API key")
        elif http_error.code == 404: 
            sys.exit("Sorry, there is no weather data for this city.")
        else:
            sys.exit("Something went wrong. Please try again! ({http_error.code})")

    data = response.read()
    try:
        return json.loads(data)
    except json.JSONDecodeError:
        sys.exit("Couldn't parse the server response. Try again.")

# def display_weather(weather_data, metric=False):
#     weather_dict = {}
#     city = weather_data["name"]
#     weather_description = weather_data["weather"][0]["description"]
#     temperature = weather_data["main"]["temp"]
#     feels_like = weather_data['main']['feels_like']
#     return {city: weather_data["name"], 
#             weather_description: weather_data["weather"][0]["description"], 
#             temperature: weather_data["main"]["temp"], 
#             feels_like: weather_data['main']['feels_like']}


def get_time(epoch_time):
    my_time = time.strftime('%I:%M %p', time.localtime(epoch_time))
    return my_time

def get_country(country_code):
    my_country = pycountry.countries.get(alpha_2=country_code)
    my_country_name = my_country.name
    my_country_flag = my_country.flag
    my_country_total = my_country_name + " " + my_country_flag
    return my_country_total

def read_user_cli_args():
    parser = argparse.ArgumentParser(
        description = "gets the temperature and weather for a city"
    )

    parser.add_argument(
        "city",
        nargs="+",
        type=str,
        help="enter the city name"
    )

    parser.add_argument(
        "-m",
        "--metric",
        action="store_true",
        help="display the temperature in metric units"
    )

    return parser.parse_args()

def _get_api_key():
    config = ConfigParser()
    config.read("secrets.ini")
    return config["openweather"]["api_key"]

def display_weather(weather_data, metric=False):

    city = weather_data["name"]
    weather_description = weather_data["weather"][0]["description"]
    temperature = weather_data["main"]["temp"]
    units = f"°{'C' if user_args.metric else 'F'}"
    local_time = get_time(int(weather_data['dt']))
    current_time = datetime.now()
    country = get_country(weather_data['sys']['country'])
    feels_like = weather_data['main']['feels_like']

    style.change_color(style.BLUE)
    print("==============================================")
    print(f"Current time: {current_time.strftime('%I:%M %p')} || Local time: {local_time}")
    print("==============================================")
    style.change_color(style.RESET)

    print(f"The weather in...")
    
    style.change_color(style.REVERSE)
    print(f"{city}, {country}  {style.RESET:^{style.PADDING}}")

    style.change_color(style.RED)
    print(f"{weather_description}".title())
    style.change_color(style.RESET)
    print(f"{temperature} {units} (feels like {feels_like} {units})")



if __name__ == "__main__":
    user_args = read_user_cli_args()
    query_url = weather_query_builder(user_args.city, user_args.metric)
    weather_data = get_weather_data(query_url)
    
    display_weather(weather_data, user_args.metric)


    # pp(weather_data)
