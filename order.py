from __future__ import annotations

import csv
from typing import List, Union

from csv_text_builder import CsvTextBuilder
from order_builder import OrderDetailBuilderFacade


class Order:
    def __init__(self, order_detail: OrderDetailBuilderFacade,
                 order_number: str, price: float) -> None:
        self.order_detail = order_detail
        self.order_number = order_number
        self.take_method = ""
        self.address = "None"
        self.price = price

    def get_order_num(self) -> str:
        return self.order_number

    def get_order_detail(self) -> OrderDetailBuilderFacade:
        return self.order_detail

    def need_address(self) -> bool:
        return self.take_method != "pick_up"

    def set_service(self, take_method: str) -> bool:
        if take_method not in (
                'pick_up', 'in_house_delivery', 'uber_eat', 'foodora'):
            return False
        else:
            self.take_method = take_method
            return True

    def set_address(self, address: str) -> bool:
        if len(address) == 0:
            return False
        else:
            self.address = address
            return True

    def get_json_format(self) -> dict:
        return {self.order_number: {"take_method": self.take_method,
                                    "order_detail": self.order_detail.build_order_detail(),
                                    "address": self.address,
                                    "price": self.price}
                }

    def get_order_format(self) -> str:
        if self.take_method == 'foodora':
            return 'CSV'
        return 'JSON'

    def get_csv_format(self) -> List[dict]:
        result = []
        for each_item in self.order_detail.build_order_detail_body_csv():
            row_dict = {"order_number": self.order_number,
                        "take_method": self.take_method,
                        "address": self.address,
                        "price": self.price}
            row_dict.update(each_item)
            result.append(row_dict)
        return result

    def get_csv_header(self) -> List[str]:
        result = ["order_number", "take_method", "address",
                  "price"] + self.order_detail.build_order_detail_csv_header()
        return result


def get_csv_string(order: Order) -> str:
    csv_file = CsvTextBuilder()
    fieldnames = order.get_csv_header()
    writer = csv.DictWriter(csv_file, fieldnames)
    writer.writerows(order.get_csv_format())
    return ''.join(csv_file.csv_string)


"""
use factory design pattern to get csv formula or json formula
"""


class SerializerFactory:
    def serialize(self, order: Order) -> Union[str, dict, bool]:
        format_ = order.get_order_format()
        return self._get_serializer(order, format_)

    def _get_serializer(self, order: Order, format_: str):
        if format_ == 'JSON':
            return order.get_json_format()
        return get_csv_string(order)
