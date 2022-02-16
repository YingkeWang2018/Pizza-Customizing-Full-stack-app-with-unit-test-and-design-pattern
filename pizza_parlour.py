from typing import List

from flask import Flask, request
from flask_restful import Api, Resource

import order_number_generator
from load_save_files import load_file, save_file

PIZZAS = load_file("pizzas")
TOPPINGS = load_file("toppings")
DRINKS = load_file("drinks")
ORDERS = load_file("orders")
KEYWORDS = load_file("key_words")
UBER_EAT = load_file("uber_eat")
HOME_DELIVERY = load_file("in_house_delivery")
app = Flask("Assignment 2")
api = Api(app)


def generate_order_num(order_file) -> str:
    order_num = order_number_generator.get_random_string()
    while order_num in order_file:
        order_num = order_number_generator.get_random_string()
    return order_num


def get_price(category: str, quantity: int, size=None) -> float:
    if size is None:
        single_price = DRINKS[category]["price"]
    else:
        single_price = PIZZAS[category][size]
    return single_price * quantity


def handle_drink_price(drink_orders: List[dict]) -> float:
    price = 0
    for drink_order in drink_orders:
        price += get_price(drink_order["name"], drink_order["quantity"])
    return round(price, 2)


def handle_pizza_price(pizza_orders: List[dict]) -> float:
    price = 0
    for pizza_order in pizza_orders:
        price += get_price(pizza_order["type"], pizza_order["quantity"],
                           pizza_order["size"])
        for topping in pizza_order["toppings"]:
            price += TOPPINGS[topping]["price"]
    return round(price, 2)


def add_price(order: dict) -> None:
    price = 0.0
    price += handle_pizza_price(order["pizza"])
    price += handle_drink_price(order["drink"])
    order["price"] = round(price, 2)


class Menu(Resource):
    def get(self, category=None, item=None):

        menu = {"pizzas": PIZZAS,
                "toppings": TOPPINGS,
                "drinks": DRINKS}

        if category is None:
            return menu, 200
        if category in menu:
            if item is None:
                return menu[category], 200
            elif item in menu[category]:
                return menu[category][item], 200
        return {}, 404


class Order(Resource):
    def post(self):
        new_order = request.get_json()
        add_price(new_order)
        new_order_num = generate_order_num(ORDERS)
        ORDERS[new_order_num] = new_order
        save_file("orders", ORDERS)
        return {"new order": {new_order_num: new_order}}

    def delete(self, order_num):
        if order_num in ORDERS:
            remove_value = ORDERS.pop(order_num)
            save_file("orders", ORDERS)
            return {order_num: remove_value}, 200
        return {}, 404

    def patch(self, order_num):
        updated_order = request.get_json()
        add_price(updated_order)
        ORDERS[order_num] = updated_order
        save_file("orders", ORDERS)
        return {order_num: ORDERS[order_num]}, 200

    def get(self, order_num):
        if order_num in ORDERS:
            return {order_num: ORDERS[order_num]}, 200
        return {}, 404


class Delivery(Resource):
    def post(self, delivery_method):
        if delivery_method == "foodora":
            data = request.data.decode('UTF-8')
            print("data: {}".format(data))
            save_file(delivery_method, data)
        else:
            data = request.get_json()
            order_num = list(data.keys())[0]

            print("data: {}".format(data))
            if delivery_method == "uber_eat":
                UBER_EAT[order_num] = data[order_num]
                save_file(delivery_method, UBER_EAT)
            else:
                HOME_DELIVERY[order_num] = data[order_num]
                save_file(delivery_method, HOME_DELIVERY)

        return {"message": "receive the delivery!"}, 200


class KeyWords(Resource):
    def get(self):
        return KEYWORDS


api.add_resource(Menu, '/menu', '/menu/<string:category>',
                 '/menu/<string:category>/<string:item>')
api.add_resource(Order, "/order", "/order/<string:order_num>")
api.add_resource(Delivery, "/delivery/<string:delivery_method>")
api.add_resource(KeyWords, "/keywords")

if __name__ == "__main__":
    app.run()
