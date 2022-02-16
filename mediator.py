from __future__ import annotations

from typing import Optional, Tuple

from client_dao import ClientDaoJson
from data_keywords_loader import DataKeyWordsLoader
from order import Order, SerializerFactory
from order_builder import Drink, OrderDetailBuilderFacade, Pizza

"""
use Mediator Design pattern to loosen the dependency between client.py (front end) with the clientDao (backend)
"""


class CreateOrderMediator:
    def __init__(self):
        self.order_detail = OrderDetailBuilderFacade()
        self.temp_pizza = Pizza()
        self.temp_drink = Drink()

    def get_temp_pizza(self) -> Pizza:
        return self.temp_pizza

    def get_temp_drink(self) -> Drink:
        return self.temp_drink

    def handle_item_quantity(self, quantity, category: str) -> bool:
        try:
            int(quantity)
        except ValueError:
            return False
        else:
            if int(quantity) <= 0:
                return False
            else:
                if category == "pizza":
                    self.temp_pizza.add_quantity(int(quantity))
                else:
                    self.temp_drink.add_quantity(int(quantity))
                return True

    def add_pizza_to_order(self) -> None:
        self.order_detail.add_pizza_to_order(self.temp_pizza)
        self.temp_pizza = Pizza()

    def add_drink_to_order(self) -> None:
        self.order_detail.add_drink_to_order(self.temp_drink)
        self.temp_drink = Drink()

    def build_order_detail(self) -> str:
        order_detail = self.order_detail.build_order_detail()
        if order_detail["pizza"] == [] and order_detail["drink"] == []:
            return "You did not order anything, thank you for coming!"
        else:
            response = ClientDaoJson.send_created_order(order_detail)
            order_num = list(response.keys())[0]
            result = ["create order with order number: {} \n".format(order_num)]
            result.append("price: {}\n".format(response[order_num]["price"]))
            result.append(self.order_detail.__str__())
            return ''.join(result)


class DeliveryMediator:
    def __init__(self):
        self.order = None

    def get_order(self, order_number: str) -> Optional[Order]:
        new_order = ClientDaoJson.get_order(order_number)
        if new_order is None:
            self.order = None
        else:
            self.order = new_order
            return self.order

    def send_file(self) -> None:
        factory = SerializerFactory()
        send_form = factory.serialize(self.order)
        ClientDaoJson.delete_order(self.order.get_order_num())
        if self.order.take_method == 'foodora':
            ClientDaoJson.send_foodora(send_form)
        else:
            ClientDaoJson.send_not_foodora(self.order.take_method, send_form)
        print("The order that get send to {} is: {}".format(
            self.order.take_method, send_form))
        print("Your order is on its way!")


class DeleteOrderMediator:
    @staticmethod
    def handle_delete_order(order_number: str) -> str:
        response = ClientDaoJson.delete_order(order_number)
        if len(response) == 0:
            return "no such order exist"
        else:
            return 'order {} with order detail {} get deleted'.format(
                order_number, response)


class UpdateOrderMediator:
    def __init__(self):
        self.order = None

    def get_order(self, order_number: str):
        new_order = ClientDaoJson.get_order(order_number)
        if new_order is None:
            self.order = None
        else:
            self.order = new_order

    def __str__(self):
        rep = f"Order Number: {self.order.get_order_num()}\n"
        rep += f"Order Details: \n{self.order.get_order_detail().__str__()}"
        return rep

    def get_length(self, category):
        if category == "pizza":
            return len(self.order.get_order_detail().pizza_order_builder.items)
        elif category == "drink":
            return len(self.order.get_order_detail().drink_order_builder.items)

    def set_item(self, category, item_num, component, value):
        if category == "pizza":
            self.order.get_order_detail().pizza_order_builder.items[
                item_num].set_component(component, value)
        elif category == "drink":
            self.order.get_order_detail().drink_order_builder.items[
                item_num].set_component(component, value)

    def delete_item(self, category, item_num):
        if category == "pizza":
            self.order.get_order_detail().pizza_order_builder.items.pop(
                item_num)
        elif category == "drink":
            self.order.get_order_detail().drink_order_builder.items.pop(
                item_num)

    def set_order(self, order_number: str):
        ClientDaoJson.set_order(order_number,
                                self.order.get_order_detail().build_order_detail())


class MenuMediator:
    def __init__(self):
        self.category = None
        self.item = None
        self.layer = 0

    def set_layer(self, layer: int):
        self.layer = layer

    def set_category(self, category: str):
        self.category = category

    def set_item(self, item: str):
        self.item = item

    def get_correspond_menu(self) -> str:
        menu = ClientDaoJson.get_menu(self.category, self.item)
        if self.category is None:
            result = ["full menu for the restaurant is:\n"]
            for category in DataKeyWordsLoader.get_menu_category_keys():
                if category != 'q':
                    menu_mediator = MenuMediator()
                    menu_mediator.set_layer(1)
                    menu_mediator.set_category(category)
                    result.append(menu_mediator.get_correspond_menu())
            return ''.join(result)

        if self.item is None:
            if len(menu) == 0:
                return "there is no such category in menu"
            else:
                result = [
                    '\t' * self.layer + f'{self.category} category menu:\n']
                for item in menu:
                    item_str = format_item(item, menu[item], self.category,
                                           self.layer + 1)
                    result.append(item_str)
                return ''.join(result)

        else:
            if len(menu) == 0:
                return "there is no such item under category {} in menu".format(
                    self.category)
            else:
                return format_item(self.item, menu, self.category, self.layer)

    def get_correspond_item_keys(self) -> Tuple[str]:
        if self.category == 'pizza':
            return DataKeyWordsLoader.get_pizza_type_keys()
        elif self.category == 'drink':
            return DataKeyWordsLoader.get_drink_name_keys()
        else:
            return DataKeyWordsLoader.get_pizza_topping_keys()


def format_item(item: str, item_dict: dict, category: str, layer: int) -> str:
    if category == 'pizza':
        return format_pizza_item(item, item_dict, layer)
    else:
        return format_drink_topping_item(item, item_dict, layer)


def format_pizza_item(item: str, item_dict: dict, layer: int) -> str:
    prices_str = ['\t' * layer + item + ':\n']
    for size_ in item_dict:
        prices_str.append(
            '\t' * (layer + 1) +
            f'price of {size_} size is {item_dict[size_]}\n')
    return ''.join(prices_str)


def format_drink_topping_item(item: str, item_dict: dict, layer: int) -> str:
    return "\t" * layer + f'price of {item} is {item_dict["price"]}\n'
