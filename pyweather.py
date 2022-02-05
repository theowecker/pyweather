# main, pyweather.py

import argparse
from configparser import ConfigParser

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
    print(user_args.city, user_args.metric)

