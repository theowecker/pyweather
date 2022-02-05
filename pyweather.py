# main, pyweather.py

import argparse
import json
import pycountry
import sys
import time
from configparser import ConfigParser
from datetime import datetime
from pprint import pp
from urllib import error, parse, request

# TODO: Add an arrow for wind direction... if 20 > deg > 60 NW arrow,
# if 60 > deg > 120 W arrow... or make dynamic arrow?

WEATHER_API_URL = "https://api.openweathermap.org/data/2.5/weather"

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


if __name__ == "__main__":
    user_args = read_user_cli_args()
    query_url = weather_query_builder(user_args.city, user_args.metric)
    weather_data = get_weather_data(query_url)
    units = f"°{'C' if user_args.metric else 'F'}"
    local_time = get_time(int(weather_data['dt']))
    current_time = datetime.now()
    country = get_country(weather_data['sys']['country'])

    # pp(weather_data)
    print(f"Current time: {current_time.strftime('%I:%M %p')} Local time: {local_time} \n")
    print(f"The weather in {weather_data['name']}, {country}")
    print(f"{weather_data['weather'][0]['description']}".title())
    print(f"{weather_data['main']['temp']} {units} (feels like {weather_data['main']['feels_like']} {units})")
