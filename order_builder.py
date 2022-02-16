from __future__ import annotations

from typing import List, Union

"""
use builder Design Pattern as well as Facade Design Pattern to build order detail
"""


class OrderDetailBuilderFacade:
    def __init__(self):
        self.pizza_order_builder = PizzaOrderBuilder()
        self.drink_order_builder = DrinkOrderBuilder()

    def create_new_pizza(self) -> Pizza:
        return self.pizza_order_builder.create_new_pizza()

    def create_new_drink(self) -> Drink:
        return self.drink_order_builder.create_new_drink()

    def add_pizza_to_order(self, pizza: Pizza) -> None:
        self.pizza_order_builder.add_item_to_order(pizza)

    def add_drink_to_order(self, drink: Drink) -> None:
        self.drink_order_builder.add_item_to_order(drink)

    def build_order_detail(self) -> dict:
        order_detail = {}
        pizza_orders = self.pizza_order_builder.get_dict_representation()
        drink_orders = self.drink_order_builder.get_dict_representation()

        order_detail["pizza"] = pizza_orders
        order_detail["drink"] = drink_orders

        return order_detail

    def build_from_json(self, order_detail: dict) -> None:
        self.pizza_order_builder.build_from_json(order_detail["pizza"])
        self.drink_order_builder.build_from_json(order_detail["drink"])

    def build_order_detail_body_csv(self) -> List[dict]:
        return self.pizza_order_builder.get_csv_dict_represent() + \
               self.drink_order_builder.get_csv_dict_represent()

    def build_order_detail_csv_header(self) -> List[str]:
        return ["order_detail/category",
                "order_detail/type",
                "order_detail/size",
                "order_detail/toppings",
                "order_detail/quantity"]

    def __str__(self):
        rep = "Pizza(s):"
        rep += self.pizza_order_builder.__str__()
        rep += "\nDrink(s):"
        rep += self.drink_order_builder.__str__()
        return rep


class OrderBuilder:
    def __init__(self):
        self.items = []

    def add_item_to_order(self, item: Item) -> None:
        self.items.append(item)

    def get_dict_representation(self) -> list:
        return [item.get_dict_represent() for item in self.items]

    def get_csv_dict_represent(self) -> [List[dict]]:
        return [item.write_to_csv_dict() for item in self.items]

    def build_from_json(self, items_json: List[dict]) -> None:
        raise NotImplementedError

    def __str__(self):
        rep = ""
        for index in range(len(self.items)):
            rep += f"\nItem number {index}: {self.items[index].__str__()}"
        return rep


class PizzaOrderBuilder(OrderBuilder):

    def build_from_json(self, items_json: List[dict]) -> None:
        for item_json in items_json:
            pizza = Pizza()
            pizza.build_from_json(item_json)
            self.add_item_to_order(pizza)

    def create_new_pizza(self) -> Union[Pizza, bool]:
        new_pizza = Pizza()
        return new_pizza


class DrinkOrderBuilder(OrderBuilder):

    def build_from_json(self, items_json: List[dict]) -> None:
        for item_json in items_json:
            drink = Drink()
            drink.build_from_json(item_json)
            self.add_item_to_order(drink)

    def create_new_drink(self) -> Drink:
        return Drink()


class Item:
    def __init__(self):
        self.type = None
        self.quantity = 0

    def _add_type(self, type_: str) -> None:
        self.type = type_

    def add_quantity(self, quantity: int) -> None:
        self.quantity = quantity

    def build_from_json(self, item_json: dict) -> None:
        self.quantity = item_json["quantity"]

    def get_dict_represent(self) -> dict:
        raise NotImplementedError

    def write_to_csv_dict(self) -> dict:
        raise NotImplementedError

    def set_component(self, component, value) -> None:
        raise NotImplementedError


class Pizza(Item):
    def __init__(self):
        super().__init__()
        self.size = None
        self.toppings = []

    def add_pizza_type(self, type_: str) -> None:
        self._add_type(type_)

    def set_size(self, size: str) -> True:
        self.size = size

    def add_toppings(self, new_topping: str, options) -> False:
        # no topping should appear twice
        if new_topping in options and \
                new_topping not in self.toppings:
            self.toppings.append(new_topping)
            return True
        else:
            return False

    def get_dict_represent(self) -> dict:
        return {
            "type": self.type,
            "size": self.size,
            "toppings": self.toppings,
            "quantity": self.quantity
        }

    def write_to_csv_dict(self) -> dict:
        return {
            "order_detail/category": "pizza",
            "order_detail/type": self.type,
            "order_detail/size": self.size,
            "order_detail/toppings": ','.join(self.toppings),
            "order_detail/quantity": self.quantity
        }

    def build_from_json(self, item_json: dict) -> None:
        super().build_from_json(item_json)
        self.type = item_json["type"]
        self.size = item_json["size"]
        self.toppings = item_json["toppings"]

    def set_component(self, component, value):
        if component == "type":
            self.type = value
        elif component == "size":
            self.size = value
        elif component == "toppings":
            self.toppings = value
        elif component == "quantity":
            self.quantity = value

    def __str__(self):
        return f"type: {self.type}, size: {self.size}," \
            f" toppings: {','.join(self.toppings)}, quantity: {self.quantity}"


class Drink(Item):
    def write_to_csv_dict(self) -> dict:
        return {
            "order_detail/category": "drink",
            "order_detail/type": self.type,
            "order_detail/size": None,
            "order_detail/toppings": None,
            "order_detail/quantity": self.quantity
        }

    def add_drink_type(self, type_: str) -> None:
        self._add_type(type_)

    def get_dict_represent(self) -> dict:
        return {"name": self.type,
                "quantity": self.quantity}

    def build_from_json(self, item_json: dict) -> None:
        super().build_from_json(item_json)
        self.type = item_json["name"]

    def set_component(self, component, value):
        if component == "name":
            self.type = value
        elif component == "quantity":
            self.quantity = value

    def __str__(self):
        return f"name: {self.type}, quantity: {self.quantity}"
