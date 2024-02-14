"""
Made by Ilyamiro

GitHub: ilyamiro/Fighter
"""

import math
import os
import sys
from typing import Union


def get_age(age):
    if not 6 < age <= 100:
        raise ValueError("Incorrect age")
    if 9 <= age <= 14:
        result = age / 10 * 1.6
    elif 14 < age <= 22:
        result = math.exp(age * 0.06)
    elif 22 < age <= 28:
        result = 3.7
    elif 28 < age <= 40:
        result = 2 + pow(2.4, age * 0.02)
    elif 40 < age <= 55:
        result = 5.7 - math.exp(age * 0.015)
    elif 55 < age <= 65:
        result = 6.3 - math.exp(age * 0.021)
    elif 65 < age < 92:
        result = 5.7 - (math.exp(age * 0.022) * 0.7)
    else:
        result = 0

    return round(result, 1)


def get_weight(weight):
    if 35 <= weight <= 140:
        return round(weight * 0.0285714286, 1)
    elif weight < 35:
        return 1.0
    elif weight > 140:
        return 4.0


def get_height(height):
    if height < 140:
        return 1
    elif 140 <= height <= 150:
        return round(math.exp(height * 0.009) - 2.5, 1)
    elif 150 < height <= 170:
        return round(math.exp(height * 0.011) - 3.9, 1)
    elif 170 < height <= 185:
        return round(math.exp(height * 0.0118) - 4.8, 1)
    elif 185 < height <= 195:
        return 4.7
    elif 195 < height <= 210:
        return round(math.exp(height * 0.006) + 1.6, 1)
    else:
        return 5.1


def scale_to_linear(value, min_original, max_original, min_linear=0, max_linear=10):
    """ A function to help scale the approximate evaluation to a linear 1-10 scale"""
    # First, normalize the value between 0 and 1 based on the original scale
    normalized_value = (value - min_original) / (max_original - min_original)
    # Then, scale the normalized value to the new linear range
    scaled_value = min_linear + (max_linear - min_linear) * normalized_value
    return scaled_value


def get_index(age: int, height: int, weight: int, skill: int, sex: str) -> int:
    """

    :param age: Age of a person in years
    :param height: Height of a person in centimeters
    :param weight: Weight of a person in kilograms
    :param skill: An approximate fight skill's index of a person on a scale from 1 to 10
    :param sex: Sex: male or female.
    :return: A relative number between 1 and 10. Fight index
    """
    fight_index = round(scale_to_linear(
        get_age(age) * 1.2 + get_height(height) * 0.9 + get_weight(weight) * 1.1 + skill * 1.3, 1, 26.79),
                        2)
    return fight_index if sex.upper() == "M" else round(fight_index * 0.55, 1)


# Text colors
red = "\033[31m"
yellow = "\033[33m"
green = "\033[32m"

# Reset
reset = "\033[0m"

# default values
default_values = {
    "age": 25,
    "weight": 75,
    "height": 175,
    "skill": 5,
    "iq": 100,
    "gender": "M"
}


def validate_input(prompt: str, default: Union[int, str], validator=lambda x: True, converter=int) -> Union[int, str]:
    value = input(prompt).replace(" ", "")
    if value.strip() == "":
        print(f"defaulting to {default}")
        return default
    try:
        value = converter(value)
        if validator(value):
            return value
    except ValueError:
        pass
    print(f"Incorrect value, defaulting to {default}")
    return default


while True:
    os.system("clear") if sys.platform == "linux" or sys.platform == "darwin" else os.system("cls")
    print(f"""{red}
  __ _       _     _
 / _(_)     | |   | |
| |_ _  __ _| |__ | |_ ___ _ __
|  _| |/ _` | '_ \| __/ _ \ '__|
| | | | (_| | | | | ||  __/ |
|_| |_|\__, |_| |_|\__\___|_|
        __/ |
       |___/

A very simple tool to estimate someone's ability to fight on a scale from 1 to 10
{yellow}GitHub: https://github.com/ilyamiro/Fighter{reset}""")
    age = validate_input("Enter age: ", default_values["age"], lambda x: x >= 0)
    sex = validate_input("Enter sex (F/M): ", default_values["gender"], lambda x: x.upper() in ["F", "M"], str)
    height = validate_input("Enter subject's height (cm): ", default_values["height"], lambda x: x > 0)
    weight = validate_input("Enter subject's weight (kg): ", default_values["weight"], lambda x: x > 0)
    skill = validate_input("Enter an estimated fight skill level (1-10): ", default_values["skill"],
                           lambda x: 1 <= x <= 10)
    print("Estimated fight index is: ", green, get_index(age, height, weight, skill, sex), reset, sep="")
    input(f"{red}Press enter to reset{reset}")
