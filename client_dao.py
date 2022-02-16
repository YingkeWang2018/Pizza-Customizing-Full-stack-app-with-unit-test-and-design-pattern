import abc
from typing import Optional

import requests

from order import Order
from order_builder import OrderDetailBuilderFacade

BASE = " http://127.0.0.1:5000/"

"""
implement DAO Design pattern to get data from server 
"""


class ClientDaoInterface(metaclass=abc.ABCMeta):
    @staticmethod
    @abc.abstractmethod
    def get_menu(category, item) -> str:
        raise NotImplementedError

    @staticmethod
    @abc.abstractmethod
    def get_order(order_num: str) -> Order:
        raise NotImplementedError

    @staticmethod
    @abc.abstractmethod
    def delete_order(order_num) -> dict:
        raise NotImplementedError

    @staticmethod
    @abc.abstractmethod
    def send_created_order(order_detail) -> dict:
        raise NotImplementedError

    @staticmethod
    @abc.abstractmethod
    def set_order(order_number: str, updated_order):
        raise NotImplementedError

    @staticmethod
    @abc.abstractmethod
    def send_foodora(send_form) -> None:
        raise NotImplementedError

    @staticmethod
    @abc.abstractmethod
    def send_not_foodora(take_method, send_form) -> None:
        raise NotImplementedError


class ClientDaoJson(ClientDaoInterface):
    @staticmethod
    def get_order(order_num: str) -> Optional[Order]:
        response = requests.get(BASE + f'/order/{order_num}').json()
        if response:
            new_order_detail = OrderDetailBuilderFacade()
            new_order_detail.build_from_json(response[order_num])
            new_order = Order(new_order_detail, order_num,
                              response[order_num]["price"])
            return new_order

    @staticmethod
    def get_menu(category: str, item: str) -> dict:
        if category is None:
            response = requests.get(BASE + '/menu')
            return response.json()
        category = category.lower()
        if category[-1] != 's':
            category += 's'
        if item is None:
            response = requests.get(BASE + f'/menu/{category}')
        else:
            item = item.lower()
            response = requests.get(BASE + f'/menu/{category}/{item}')
        return response.json()

    @staticmethod
    def send_created_order(order_detail) -> dict:
        response = requests.post(BASE + '/order', json=order_detail).json()
        return response['new order']

    @staticmethod
    def set_order(order_number: str, updated_order):
        requests.patch(BASE + f'/order/{order_number}', json=updated_order)

    @staticmethod
    def delete_order(order_num) -> dict:
        response = requests.delete(BASE + f'/order/{order_num}').json()
        return response

    @staticmethod
    def send_foodora(send_form) -> None:
        requests.post(BASE + "delivery/{}".format("foodora"),
                      data=send_form)

    @staticmethod
    def send_not_foodora(take_method, send_form) -> None:
        requests.post(BASE + "delivery/{}".format(take_method),
                      json=send_form)
