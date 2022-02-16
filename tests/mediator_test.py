from unittest.mock import patch

import pytest

from data_keywords_loader import DataKeyWordsLoader
from mediator import CreateOrderMediator, DeleteOrderMediator, DeliveryMediator, \
    MenuMediator, UpdateOrderMediator
from order import Order
from order_builder import Drink, OrderDetailBuilderFacade, Pizza

TEMP_KEYWORDS = {
    "CATEGORY_KEYWORDS": [
        "pizza",
        "drink",
        "q"
    ],
    "PIZZA_COMPONENTS_KEYWORDS": [
        "type",
        "size",
        "toppings",
        "quantity",
        "q"
    ],
    "DRINK_COMPONENTS_KEYWORDS": [
        "name",
        "quantity",
        "q"
    ],
    "PIZZA_TYPE_KEYWORDS": [
        "pepperoni",
        "margherita",
        "vegetarian",
        "neapolitan",
        "q"
    ],
    "PIZZA_SIZE_KEYWORDS": [
        "s",
        "m",
        "l",
        "q"
    ],
    "PIZZA_TOPPING_KEYWORDS": [
        "olives",
        "tomatoes",
        "mushrooms",
        "jalapenos",
        "chicken",
        "beef",
        "pepperoni",
        "q"
    ],
    "DRINK_NAME_KEYWORDS": [
        "coke",
        "diet coke",
        "coke zero",
        "pepsi",
        "diet pepsi",
        "dr. pepper",
        "water",
        "juice",
        "q"
    ],
    "MENU_CATEGORY_KEYWORDS": [
        "pizza",
        "drink",
        "topping",
        "q"
    ]
}


# Class CreateOrderMediator
def test_get_temp_pizza():
    mediator = CreateOrderMediator()
    assert isinstance(mediator.get_temp_pizza(), Pizza) is True


def test_get_temp_drink():
    mediator = CreateOrderMediator()
    assert isinstance(mediator.get_temp_drink(), Drink) is True


def test_handle_item_quantity():
    mediator = CreateOrderMediator()
    assert mediator.handle_item_quantity("A", "pizza") is False
    assert mediator.handle_item_quantity("0", "pizza") is False
    assert mediator.handle_item_quantity("1", "pizza") is True
    assert mediator.temp_pizza.quantity == 1
    assert mediator.handle_item_quantity("2", "drink") is True
    assert mediator.temp_drink.quantity == 2


def test_add_pizza_to_order():
    mediator = CreateOrderMediator()
    pizza = mediator.get_temp_pizza()
    mediator.add_pizza_to_order()
    assert mediator.order_detail.pizza_order_builder.items[0] == pizza


def test_add_drink_to_order():
    mediator = CreateOrderMediator()
    drink = mediator.get_temp_drink()
    mediator.add_drink_to_order()
    assert mediator.order_detail.drink_order_builder.items[0] == drink


@patch('requests.post')
def test_build_order_detail(mock_post):
    mediator = CreateOrderMediator()
    assert mediator.build_order_detail() == "You did not order anything, thank you for coming!"
    mediator.add_pizza_to_order()
    mediator.add_drink_to_order()
    mock_post.return_value.json.return_value = {
        "new order": {"abcdef": {
            "pizza": [
                {
                    "type": None,
                    "size": None,
                    "toppings": [],
                    "quantity": 0
                }
            ],
            "drink": [
                {
                    "name": None,
                    "quantity": 0
                }
            ],
            "price": 0.00
        }}}
    assert mediator.build_order_detail() is not None


# Class DeliveryMediator
@patch('requests.get')
def test_delivery_mediator_get_order(mock_get):
    mediator = DeliveryMediator()
    mediator.get_order("0")
    assert mediator.order is not None
    mock_get.return_value.json.return_value = {}
    mediator.get_order("1111")
    assert mediator.order is None


@patch('requests.post')
@patch('requests.delete')
def test_send_file(mock_delete, mock_post):
    mediator1 = DeliveryMediator()
    order_detail = OrderDetailBuilderFacade()
    mediator1.order = Order(order_detail, "abcdef", 15.99)
    assert mediator1.send_file() is None
    mediator2 = DeliveryMediator()
    order_detail = OrderDetailBuilderFacade()
    mediator2.order = Order(order_detail, "abcdef", 15.99)
    mediator2.order.take_method = 'foodora'
    assert mediator2.send_file() is None


# Class DeleteOrderMediator
@patch('requests.delete')
def test_handle_delete_order(mock_delete):
    mediator = DeleteOrderMediator()
    assert mediator.handle_delete_order("111111") == "no such order exist"
    mock_delete.return_value.json.return_value = {"abcdef": {}}
    assert mediator.handle_delete_order(
        "abcdef") == "order abcdef with order detail {'abcdef': {}} get deleted"


# Class UpdateOrderMediator
@patch('requests.get')
def test_update_order_mediator_get_order(mock_get):
    mediator = UpdateOrderMediator()
    mediator.get_order("0")
    assert mediator.order is not None
    mock_get.return_value.json.return_value = {}
    mediator.get_order("1111")
    assert mediator.order is None


def test_str():
    mediator = UpdateOrderMediator()
    order_detail = OrderDetailBuilderFacade()
    mediator.order = Order(order_detail, "abcdef", 15.99)
    assert mediator.__str__() == "Order Number: abcdef\nOrder Details: \nPizza(s):\nDrink(s):"


def test_get_length():
    mediator = UpdateOrderMediator()
    order_detail = OrderDetailBuilderFacade()
    mediator.order = Order(order_detail, "abcdef", 15.99)
    assert mediator.get_length("pizza") == 0
    assert mediator.get_length("drink") == 0


def test_update_order_mediator_set_item():
    mediator = UpdateOrderMediator()
    order_detail = OrderDetailBuilderFacade()
    pizza = order_detail.create_new_pizza()
    order_detail.add_pizza_to_order(pizza)
    drink = order_detail.create_new_drink()
    order_detail.add_drink_to_order(drink)
    mediator.order = Order(order_detail, "abcdef", 15.99)
    mediator.set_item("pizza", 0, "type", "blank")
    mediator.set_item("drink", 0, "name", "coke")
    assert mediator.order.order_detail.pizza_order_builder.items[
               0].type == "blank"
    assert mediator.order.order_detail.drink_order_builder.items[
               0].type == "coke"


def test_delete_item():
    mediator = UpdateOrderMediator()
    order_detail = OrderDetailBuilderFacade()
    pizza = order_detail.create_new_pizza()
    order_detail.add_pizza_to_order(pizza)
    drink = order_detail.create_new_drink()
    order_detail.add_drink_to_order(drink)
    mediator.order = Order(order_detail, "abcdef", 15.99)
    assert len(mediator.order.order_detail.pizza_order_builder.items) == 1
    assert len(mediator.order.order_detail.drink_order_builder.items) == 1
    mediator.delete_item("pizza", 0)
    mediator.delete_item("drink", 0)
    assert mediator.order.order_detail.pizza_order_builder.items == []
    assert mediator.order.order_detail.drink_order_builder.items == []


@patch('requests.patch')
def test_set_order(mock_patch):
    mediator = UpdateOrderMediator()
    order_detail = OrderDetailBuilderFacade()
    pizza = order_detail.create_new_pizza()
    order_detail.add_pizza_to_order(pizza)
    drink = order_detail.create_new_drink()
    order_detail.add_drink_to_order(drink)
    mediator.order = Order(order_detail, "abcdef", 15.99)
    assert mediator.set_order("abcdef") is None


# Class MenuMediator
def test_set_layer():
    mediator = MenuMediator()
    mediator.set_layer(1)
    assert mediator.layer == 1


def test_set_category():
    mediator = MenuMediator()
    mediator.set_category("pizza")
    assert mediator.category == "pizza"


def test_menu_mediator_set_item():
    mediator = MenuMediator()
    mediator.set_item("coke")
    assert mediator.item == "coke"


@patch('requests.get')
def test_get_correspond_menu(mock_get):
    mock_get.return_value.json.return_value = TEMP_KEYWORDS
    DataKeyWordsLoader.load_keywords()
    mediator = MenuMediator()
    mock_get.return_value.json.return_value = {}
    assert mediator.get_correspond_menu() == "full menu for the restaurant is:" \
                                             "\nthere is no such category in menuthere is no such category in menuthere is no such category in menu"
    mediator.category = "pizza"
    assert mediator.get_correspond_menu() == "there is no such category in menu"
    mock_get.return_value.json.return_value = {
        "pepperoni": {
            "s": 8.99,
            "m": 9.99,
            "l": 10.99
        }
    }
    assert mediator.get_correspond_menu() == "pizza category menu:\n\tpepperoni:" \
                                             "\n\t\tprice of s size is 8.99" \
                                             "\n\t\tprice of m size is 9.99" \
                                             "\n\t\tprice of l size is 10.99\n"
    mock_get.return_value.json.return_value = {
        "coke": {
            "price": 1.99
        }
    }
    mediator.category = "drink"
    assert mediator.get_correspond_menu() == "drink category menu:\n\tprice of coke is 1.99\n"
    mediator.item = "coke"
    mock_get.return_value.json.return_value = {"price": 1.99}
    assert mediator.get_correspond_menu() == "price of coke is 1.99\n"
    mock_get.return_value.json.return_value = {}
    assert mediator.get_correspond_menu() == "there is no such item under category drink in menu"


@patch('requests.get')
def test_get_correspond_item_keys(mock_get):
    mock_get.return_value.json.return_value = TEMP_KEYWORDS
    DataKeyWordsLoader.load_keywords()
    mediator = MenuMediator()
    assert mediator.get_correspond_item_keys() == ("olives",
                                                   "tomatoes",
                                                   "mushrooms",
                                                   "jalapenos",
                                                   "chicken",
                                                   "beef",
                                                   "pepperoni",
                                                   "q")
    mediator.category = "pizza"
    assert mediator.get_correspond_item_keys() == ("pepperoni",
                                                   "margherita",
                                                   "vegetarian",
                                                   "neapolitan",
                                                   "q")
    mediator.category = "drink"
    assert mediator.get_correspond_item_keys() == ("coke",
                                                   "diet coke",
                                                   "coke zero",
                                                   "pepsi",
                                                   "diet pepsi",
                                                   "dr. pepper",
                                                   "water",
                                                   "juice",
                                                   "q")


if __name__ == '__main__':
    pytest.main(["mediator_test.py"])
