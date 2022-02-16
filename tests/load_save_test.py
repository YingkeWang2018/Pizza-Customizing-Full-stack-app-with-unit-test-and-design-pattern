import json

import pytest

from load_save_files import load_file, save_file
from tests.conftest import DRINK, PIZZAS


def test_load_pizza_file():
    pizza_dict = load_file('pizzas')
    assert pizza_dict == PIZZAS


def test_load_drink_file():
    drink_dict = load_file("drinks")
    assert drink_dict == DRINK


temp_order = {"yebtdjcr": {
    "pizza": [
        {
            "type": "vegetarian",
            "size": "l",
            "toppings": [],
            "quantity": 2
        }
    ],
    "drink": [
        {
            "name": "water",
            "quantity": 2
        }
    ],
    "price": 47.96
}}


def test_save_order_file(load_order_file):
    save_file("orders", temp_order)
    input_file = open("order.json", "r")
    file_dict = json.load(input_file)
    assert "yebtdjcr" in file_dict


foodora_str = '\n0,foodora,hdeiohwoe,46.92,pizza,pepperoni,s,"tomatoes,mushrooms",1\n0,foodora,hdeiohwoe,46.92,pizza' \
              ',margherita,m,"jalapenos,chicken",2\n0,foodora,hdeiohwoe,46.92,drink,dr. pepper,,,1'


def test_save_foodora_file(load_delivery_files):
    save_file("foodora", foodora_str)
    input_file = open("foodora.csv", "r")
    str_ = input_file.read()
    assert foodora_str in str_


if __name__ == "__main__":
    pytest.main(['load_save_test.py'])
