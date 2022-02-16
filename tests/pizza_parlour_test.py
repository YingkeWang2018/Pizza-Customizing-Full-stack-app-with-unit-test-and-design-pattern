import json

import pytest

from pizza_parlour import add_price, app, generate_order_num, get_price, \
    handle_drink_price, handle_pizza_price


def load_order() -> dict:
    file = open("order.json", "r")
    return json.load(file)


def test_generate_order_num(load_order_file):
    order = load_order()
    assert generate_order_num(order) not in order


def test_pizza_get_price():
    price = get_price("margherita", 1, "l")
    assert price == 14.99


def test_drink_get_price():
    price = get_price("diet coke", 2)
    assert price == 3.98


def test_handle_drink_price():
    drink_orders = [
        {
            "name": "coke",
            "quantity": 1
        },
        {
            "name": "water",
            "quantity": 1
        }
    ]
    price = handle_drink_price(drink_orders)
    assert price == 2.98


def test_handle_pizza_price():
    pizza_orders = [
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
    ]
    price = handle_pizza_price(pizza_orders)
    assert price == 44.93


def test_add_price():
    order = {
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
        ]}
    add_price(order)
    assert order["price"] == 47.92


@pytest.fixture
def client():
    client = app.test_client()
    return client


test_menu = {
    'pizzas': {'pepperoni': {'s': 8.99, 'm': 9.99, 'l': 10.99},
               'margherita': {'s': 10.99, 'm': 12.99, 'l': 14.99},
               'vegetarian': {'s': 11.99, 'm': 13.99, 'l': 22.99},
               'neapolitan': {'s': 9.99, 'm': 10.99, 'l': 11.99},
               'blank': {'s': 5.99, 'm': 6.99, 'l': 7.99}},
    'toppings': {'olives': {'price': 1.99}, 'tomatoes': {'price': 1.99},
                 'mushrooms': {'price': 3.99},
                 'jalapenos': {'price': 0.99}, 'chicken': {'price': 2.99},
                 'beef': {'price': 4.99},
                 'pepperoni': {'price': 1.99}},
    'drinks': {'coke': {'price': 1.99}, 'diet coke': {'price': 1.99},
               'coke zero': {'price': 1.99},
               'pepsi': {'price': 1.99}, 'diet pepsi': {'price': 1.99},
               'dr. pepper': {'price': 1.99},
               'water': {'price': 0.99}, 'juice': {'price': 2.99}}}


def test_get_menu(client):
    response = client.get("/menu")
    menu = response.get_json()
    assert menu == test_menu


def test_get_pizza_menu(client):
    response = client.get("/menu/pizzas")
    pizzas = response.get_json()
    assert pizzas == test_menu["pizzas"]


def test_get_item_menu(client):
    response = client.get("/menu/pizzas/pepperoni")
    pepperoni = response.get_json()
    assert pepperoni == test_menu["pizzas"]["pepperoni"]


new_order = {
    "pizza": [
        {
            "type": "neapolitan",
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
    ]}

updated_order = {'0': {'drink': [{'name': 'juice', 'quantity': 1}], 'pizza': [
    {'quantity': 1, 'size': 's', 'toppings': ['tomatoes', 'mushrooms'],
     'type': 'neapolitan'},
    {'quantity': 2, 'size': 'm', 'toppings': ['jalapenos', 'chicken'],
     'type': 'margherita'}], 'price': 48.92}}


def test_post_order(load_order_file, client):
    response = client.post("/order", json=new_order)
    back_order = response.get_json()
    order_num = list(back_order["new order"].keys())[0]
    assert back_order["new order"][order_num]["price"] == 48.92


def test_delete_order(load_order_file, client):
    response = client.delete("/order/0")
    response = response.get_json()
    with open("order.json", "r")as f:
        dict_ = json.load(f)
        assert "0" not in dict_


def test_patch_order(load_order_file, client):
    response = client.patch("/order/0", json=new_order)
    response = response.get_json()
    assert response == updated_order


geted_order = {'0': {'drink': [{'name': 'juice', 'quantity': 1}], 'pizza': [
    {'quantity': 1, 'size': 's', 'toppings': ['tomatoes', 'mushrooms'],
     'type': 'neapolitan'},
    {'quantity': 2, 'size': 'm', 'toppings': ['jalapenos', 'chicken'],
     'type': 'margherita'}], 'price': 48.92}}


def test_get_order(load_order_file, client):
    response = client.get("/order/0").get_json()
    assert response == geted_order


foodora_msg = '\n1,foodora,hdeiohwoe,46.92,pizza,pepperoni,s,"tomatoes,mushrooms",1\n1,foodora,hdeiohwoe,46.92,pizza' \
              ',margherita,m,"jalapenos,chicken",2\n1,foodora,hdeiohwoe,46.92,drink,dr. pepper,,,1'


def test_delivery_order(load_order_file, load_delivery_files, client):
    client.post("/delivery/foodora", data=foodora_msg).get_json()
    with open("foodora.csv", "r")as f:
        s = f.read()
        assert "1" in s


def test_keyword_order(client):
    response = client.post("/keywords").get_json()
    assert len(response) != 0


if __name__ == "__main__":
    pytest.main(['pizza_parlour_test.py'])
