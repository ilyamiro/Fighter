"""
Made by Ilyamiro

GitHub: ilyamiro/Fighter
"""

import math
import os
import sys
from typing import Union


# (value, score) anchors sampled from the original hand-tuned curves, joined linearly so there are no jumps or gaps
AGE_POINTS = [(6, 1.0), (9, 1.4), (14, 2.3), (22, 3.7), (28, 3.7), (40, 3.95), (55, 3.3), (65, 2.55), (91, 0.5),
              (100, 0.0)]
HEIGHT_POINTS = [(140, 1.0), (150, 1.35), (170, 2.6), (185, 4.1), (195, 4.75), (210, 5.1)]
WEIGHT_POINTS = [(35, 1.0), (140, 4.0)]
# How much of the mass counts as fighting weight, by BMI: full in the healthy/muscular range, less when very lean or heavy
BUILD_POINTS = [(15, 0.6), (18.5, 0.9), (21, 1.0), (27, 1.0), (32, 0.85), (40, 0.65)]

# Lowest and highest possible weighted sums, so the scale can't drift out of sync with the curves above
MIN_SUM = (min(p[1] for p in AGE_POINTS) * 1.2 + min(p[1] for p in HEIGHT_POINTS) * 0.9
           + min(p[1] for p in WEIGHT_POINTS) * min(p[1] for p in BUILD_POINTS) * 1.1 + 1 * 1.3)
MAX_SUM = (max(p[1] for p in AGE_POINTS) * 1.2 + max(p[1] for p in HEIGHT_POINTS) * 0.9
           + max(p[1] for p in WEIGHT_POINTS) * max(p[1] for p in BUILD_POINTS) * 1.1 + 10 * 1.3)


def interpolate(value, points):
    """ Piecewise-linear lookup; values outside the points are clamped to the first/last score """
    if value <= points[0][0]:
        return points[0][1]
    for (x0, y0), (x1, y1) in zip(points, points[1:]):
        if value <= x1:
            return y0 + (y1 - y0) * (value - x0) / (x1 - x0)
    return points[-1][1]


def get_age(age):
    if not 6 < age <= 100:
        raise ValueError("Incorrect age")
    return interpolate(age, AGE_POINTS)


def get_weight(weight, height):
    """ Mass counts, but only as much as the build allows: the same weight is worth less on a very short or very tall frame """
    bmi = weight / (height / 100) ** 2
    return interpolate(weight, WEIGHT_POINTS) * interpolate(bmi, BUILD_POINTS)


def get_height(height):
    return interpolate(height, HEIGHT_POINTS)


def scale_to_linear(value, min_original, max_original, min_linear=0, max_linear=10):
    """ A function to help scale the approximate evaluation to a linear 1-10 scale"""
    # First, normalize the value between 0 and 1 based on the original scale
    normalized_value = (value - min_original) / (max_original - min_original)
    # Then, scale the normalized value to the new linear range
    scaled_value = min_linear + (max_linear - min_linear) * normalized_value
    return scaled_value


def get_index(age: float, height: float, weight: float, skill: float, sex: str) -> float:
    """

    :param age: Age of a person in years
    :param height: Height of a person in centimeters
    :param weight: Weight of a person in kilograms
    :param skill: An approximate fight skill's index of a person on a scale from 1 to 10
    :param sex: Sex: male or female.
    :return: A relative number between 1 and 10. Fight index
    """
    fight_index = scale_to_linear(
        get_age(age) * 1.2 + get_height(height) * 0.9 + get_weight(weight, height) * 1.1 + skill * 1.3,
        MIN_SUM, MAX_SUM, min_linear=1)
    return round(fight_index if sex.upper() == "M" else fight_index * 0.55, 1)


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


def validate_input(prompt: str, default: Union[float, str], validator=lambda x: True, converter=float) -> Union[float, str]:
    """ Blank input takes the default; anything invalid asks again instead of silently guessing """
    while True:
        value = input(prompt).replace(" ", "")
        if value == "":
            print(f"defaulting to {default}")
            return default
        try:
            value = converter(value)
            if validator(value):
                return value
        except ValueError:
            pass
        print("Incorrect value, try again (or press enter for the default)")


def main():
    while True:
        os.system("clear") if sys.platform == "linux" or sys.platform == "darwin" else os.system("cls")
        print(rf"""{red}
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
        age = validate_input("Enter age: ", default_values["age"], lambda x: 6 < x <= 100)
        sex = validate_input("Enter sex (F/M): ", default_values["gender"], lambda x: x.upper() in ["F", "M"], str)
        height = validate_input("Enter subject's height (cm): ", default_values["height"], lambda x: x > 0)
        weight = validate_input("Enter subject's weight (kg): ", default_values["weight"], lambda x: x > 0)
        skill = validate_input("Enter an estimated fight skill level (1-10): ", default_values["skill"],
                               lambda x: 1 <= x <= 10)
        print("Estimated fight index is: ", green, get_index(age, height, weight, skill, sex), reset, sep="")
        input(f"{red}Press enter to reset{reset}")


if __name__ == "__main__":
    try:
        main()
    except (KeyboardInterrupt, EOFError):
        print()
