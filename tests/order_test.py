import pytest

from order import *


# Class Order
def test_order_get_order_num():
    order_detail = OrderDetailBuilderFacade()
    client_order = Order(order_detail, "abcdef", 15.99)
    assert client_order.get_order_num() == "abcdef"


def test_order_get_order_detail():
    order_detail = OrderDetailBuilderFacade()
    client_order = Order(order_detail, "abcdef", 15.99)
    assert client_order.get_order_detail() == order_detail


def test_order_need_address():
    order_detail = OrderDetailBuilderFacade()
    client_order = Order(order_detail, "abcdef", 15.99)
    assert client_order.need_address() is True
    client_order.take_method = "pick_up"
    assert client_order.need_address() is False
    client_order.take_method = "uber_eat"
    assert client_order.need_address() is True


def test_order_set_service():
    order_detail = OrderDetailBuilderFacade()
    client_order = Order(order_detail, "abcdef", 15.99)
    assert client_order.set_service("nothing") is False
    assert client_order.set_service("foodora") is True
    assert client_order.take_method == "foodora"


def test_order_set_address():
    order_detail = OrderDetailBuilderFacade()
    client_order = Order(order_detail, "abcdef", 15.99)
    assert client_order.set_address("") is False
    assert client_order.set_address("27 King's College Cir") is True
    assert client_order.address == "27 King's College Cir"


def test_order_get_json_format():
    order_detail = OrderDetailBuilderFacade()
    client_order = Order(order_detail, "abcdef", 15.99)
    client_order.take_method = "in_house_delivery"
    client_order.address = "27 King's College Cir"
    assert client_order.get_json_format() == {
        "abcdef": {"take_method": "in_house_delivery",
                   "order_detail": {"pizza": [], "drink": []},
                   "address": "27 King's College Cir",
                   "price": 15.99}
    }


def test_order_get_order_format():
    order_detail = OrderDetailBuilderFacade()
    client_order = Order(order_detail, "abcdef", 15.99)
    client_order.take_method = "foodora"
    assert client_order.get_order_format() == "CSV"
    client_order.take_method = "uber_eat"
    assert client_order.get_order_format() == "JSON"


def test_order_get_csv_format():
    order_detail = OrderDetailBuilderFacade()
    pizza = order_detail.create_new_pizza()
    pizza.type = "blank"
    pizza.size = "s"
    pizza.toppings = ["beef", "tomatoes"]
    pizza.quantity = 2
    drink = order_detail.create_new_drink()
    drink.type = "coke"
    drink.quantity = 1
    order_detail.add_pizza_to_order(pizza)
    order_detail.add_drink_to_order(drink)
    client_order = Order(order_detail, "abcdef", 15.99)
    assert client_order.get_csv_format() == [{
        "order_number": "abcdef",
        "take_method": "",
        "address": "None",
        "price": 15.99,
        "order_detail/category": "pizza",
        "order_detail/type": "blank",
        "order_detail/size": "s",
        "order_detail/toppings": ','.join(["beef", "tomatoes"]),
        "order_detail/quantity": 2
    }, {
        "order_number": "abcdef",
        "take_method": "",
        "address": "None",
        "price": 15.99,
        "order_detail/category": "drink",
        "order_detail/type": "coke",
        "order_detail/size": None,
        "order_detail/toppings": None,
        "order_detail/quantity": 1
    }]


def test_order_get_csv_header():
    order_detail = OrderDetailBuilderFacade()
    client_order = Order(order_detail, "abcdef", 15.99)
    assert client_order.get_csv_header() == ["order_number", "take_method",
                                             "address",
                                             "price", "order_detail/category",
                                             "order_detail/type",
                                             "order_detail/size",
                                             "order_detail/toppings",
                                             "order_detail/quantity"]


# Class SerializerFactory
def test_serializer_factory_serialize():
    order_detail = OrderDetailBuilderFacade()
    client_order = Order(order_detail, "abcdef", 15.99)
    client_order.take_method = "in_house_delivery"
    client_order.address = "27 King's College Cir"
    serializer = SerializerFactory()
    assert serializer.serialize(client_order) == {
        "abcdef": {"take_method": "in_house_delivery",
                   "order_detail": {"pizza": [], "drink": []},
                   "address": "27 King's College Cir",
                   "price": 15.99}
    }
    client_order.take_method = "foodora"
    assert serializer.serialize(client_order) == ""


def test_serializer_factory_get_serializer():
    order_detail = OrderDetailBuilderFacade()
    client_order = Order(order_detail, "abcdef", 15.99)
    client_order.take_method = "in_house_delivery"
    client_order.address = "27 King's College Cir"
    serializer = SerializerFactory()
    assert serializer._get_serializer(client_order, 'JSON') == {
        "abcdef": {"take_method": "in_house_delivery",
                   "order_detail": {"pizza": [], "drink": []},
                   "address": "27 King's College Cir",
                   "price": 15.99}
    }
    client_order.take_method = "foodora"
    assert serializer._get_serializer(client_order, 'CSV') == ""


if __name__ == "__main__":
    pytest.main(['order_test.py'])
