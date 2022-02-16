import json

import pytest

PIZZAS = {
    "pepperoni": {
        "s": 8.99,
        "m": 9.99,
        "l": 10.99
    },
    "margherita": {
        "s": 10.99,
        "m": 12.99,
        "l": 14.99
    },
    "vegetarian": {
        "s": 11.99,
        "m": 13.99,
        "l": 22.99
    },
    "neapolitan": {
        "s": 9.99,
        "m": 10.99,
        "l": 11.99
    },
    "blank": {
        "s": 5.99,
        "m": 6.99,
        "l": 7.99
    }
}

DRINK = {
    "coke": {
        "price": 1.99
    },
    "diet coke": {
        "price": 1.99
    },
    "coke zero": {
        "price": 1.99
    },
    "pepsi": {
        "price": 1.99
    },
    "diet pepsi": {
        "price": 1.99
    },
    "dr. pepper": {
        "price": 1.99
    },
    "water": {
        "price": 0.99
    },
    "juice": {
        "price": 2.99
    }
}

TOPPING = {
    "olives": {
        "price": 1.99
    },
    "tomatoes": {
        "price": 1.99
    },
    "mushrooms": {
        "price": 3.99
    },
    "jalapenos": {
        "price": 0.99
    },
    "chicken": {
        "price": 2.99
    },
    "beef": {
        "price": 4.99
    },
    "pepperoni": {
        "price": 1.99
    }
}

ORDER_CONSTANT = {
    "0": {
        "pizza": [
            {
                "type": "pepperoni",
                "size": "s",
                "toppings": [
                    "tomatoes",
                    "mushrooms"
                ],
                "quantity": 1
            },
            {
                "type": "margherita",
                "size": "m",
                "toppings": [
                    "jalapenos",
                    "chicken"
                ],
                "quantity": 2
            }
        ],
        "drink": [
            {
                "name": "juice",
                "quantity": 1
            }
        ],
        "price": 47.92
    },
    "1": {
        "pizza": [
            {
                "type": "vegetarian",
                "size": "s",
                "toppings": [
                    "mushrooms"
                ],
                "quantity": 1
            }
        ],
        "drink": [
            {
                "name": "coke",
                "quantity": 1
            },
            {
                "name": "water",
                "quantity": 1
            }
        ],
        "price": 18.96
    },
    "bwzvvutv": {
        "pizza": [
            {
                "type": "vegetarian",
                "size": "s",
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
        "price": 25.96
    },
    "sweyryrp": {
        "pizza": [
            {
                "type": "pepperoni",
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
        "price": 23.96
    },
    "bcivunbj": {
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
                "name": "juice",
                "quantity": 2
            }
        ],
        "price": 51.96
    }
}


@pytest.fixture
def load_order_file():
    with open("order.json", "w") as f:
        json.dump(ORDER_CONSTANT, f)


@pytest.fixture
def load_delivery_files():
    with open("foodora.csv", "w") as f:
        f.write(
            "order_number,take_method,address,price,order_detail/category,order_detail/type,order_detail/size,order_detail/toppings,order_detail/quantity")
    with open("uberEat.json", "w") as f:
        json.dump({}, f)
    with open("restaurantDelivery.json", "w") as f:
        json.dump({}, f)


if __name__ == "__main__":
    load_delivery_files()
