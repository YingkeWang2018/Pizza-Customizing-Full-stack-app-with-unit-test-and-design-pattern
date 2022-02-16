import json
import os
from typing import Union

file_map = {
    "pizzas": 'pizza.json',
    "drinks": 'drink.json',
    'toppings': 'topping.json',
    'orders': 'order.json',
    "uber_eat": 'uberEat.json',
    "foodora": "foodora.csv",
    'in_house_delivery': "restaurantDelivery.json",
    'pick_up': "restaurantDelivery.json",
    'key_words': "restaurantKeywords.json"

}


def load_file(category: str):
    input_file = open(
        os.path.join(os.path.dirname(__file__), file_map[category]))
    file_dict = json.load(input_file)
    return file_dict


def save_file(category: str, new_file: Union[dict, str]):
    if category == 'foodora':
        with open(file_map[category], 'a') as f:
            handle_csv_str(str(new_file), f)
    else:
        with open(file_map[category], 'w') as f:
            json.dump(new_file, f)


def handle_csv_str(new_file: str, file):
    lines = new_file.splitlines()
    for line in lines:
        file.write(line + "\n")
