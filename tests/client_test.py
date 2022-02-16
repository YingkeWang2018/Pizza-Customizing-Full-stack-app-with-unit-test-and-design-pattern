from unittest import mock

import pytest

from client import ask_for_delivery, check_quit, create_drink_order, \
    create_new_order, create_pizza_order, create_single_drink, \
    create_single_pizza, delete_order, get_component, get_num, get_toppings, \
    get_value, perform_action, restaurant_operation, view_menu
from data_keywords_loader import DataKeyWordsLoader
from exception import QuitError
from mediator import CreateOrderMediator, UpdateOrderMediator
from order import Order
from order_builder import OrderDetailBuilderFacade
from tests.mock_input_output import get_display_output, set_keyboard_input


def test_check_quit():
    with pytest.raises(QuitError):
        check_quit("q")


temp_keywords = {
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


@mock.patch('data_keywords_loader.requests.get')
def test_create_single_drink(keywords):
    inputs = ["water", "-1", "2"]
    set_keyboard_input(inputs)
    keywords.return_value.json.return_value = temp_keywords
    DataKeyWordsLoader.load_keywords()
    processor = CreateOrderMediator()
    create_single_drink(processor)
    assert get_display_output() == ["Finish drink Creating!"]


@mock.patch('data_keywords_loader.requests.get')
def test_create_single_pizza(keywords):
    inputs = ["vegetarian", "s", "jalapenos", "e", "-3", "2"]
    set_keyboard_input(inputs)
    keywords.return_value.json.return_value = temp_keywords
    processor = CreateOrderMediator()
    create_single_pizza(processor)
    assert get_display_output() == ["Finish pizza Creating!"]


@mock.patch('client.create_single_drink', return_value=None)
@mock.patch('data_keywords_loader.requests.get')
def test_create_drink_order(keywords, create_single_drink):
    inputs = ["Y", "no"]
    set_keyboard_input(inputs)
    keywords.return_value.json.return_value = temp_keywords
    processor = CreateOrderMediator()
    create_drink_order(processor)
    assert get_display_output() == ["Thank you for ordering drinks!"]


@mock.patch('client.create_single_pizza', return_value=None)
@mock.patch('data_keywords_loader.requests.get')
def test_create_pizza_order(keywords, create_single_pizza):
    inputs = ["Y", "no"]
    set_keyboard_input(inputs)
    keywords.return_value.json.return_value = temp_keywords
    processor = CreateOrderMediator()
    create_pizza_order(processor)
    assert get_display_output() == ["Thank you for ordering pizzas!"]


@mock.patch('client.create_pizza_order', return_value=None)
@mock.patch('client.create_drink_order', return_value=None)
def test_create_new_order(create_pizza_order, create_drink_order):
    inputs = []
    set_keyboard_input(inputs)
    create_new_order()
    outputs = get_display_output()
    assert outputs == ['Create a New Order',
                       'You did not order anything, thank you for coming!']


def test_get_num():
    inputs = ["2"]
    set_keyboard_input(inputs)
    assert 2 == get_num(4, "test get num")


def test_pizza_get_category():
    inputs = ["type"]
    set_keyboard_input(inputs)
    assert "type" == get_component("pizza")


def test_drink_get_category():
    inputs = ["name"]
    set_keyboard_input(inputs)
    assert "name" == get_component("drink")


def test_get_toppings():
    inputs = ["tomatoes mushrooms"]
    set_keyboard_input(inputs)
    toppings = get_toppings()
    assert ["tomatoes", "mushrooms"] == toppings


def test_get_value_type():
    inputs = ["type", "pepperoni"]
    set_keyboard_input(inputs)
    value = get_value("type")
    assert value == "pepperoni"


def test_get_value_size():
    inputs = ["s"]
    set_keyboard_input(inputs)
    value = get_value("size")
    assert value == "s"


def test_get_value_others():
    inputs = ["mushrooms"]
    set_keyboard_input(inputs)
    value = get_value("toppings")
    assert value == ["mushrooms"]
    inputs = ["water"]
    set_keyboard_input(inputs)
    value = get_value("name")
    assert value == "water"
    inputs = ["2"]
    set_keyboard_input(inputs)
    value = get_value("quantity")
    assert value == 2


class OrderClass:
    order_detail = {}

    def __init__(self):
        self.order_detail = {}


class OtherClass:
    order = OrderClass()

    def set_item(self, category, item_num, component, value):
        return 1

    def get_length(self, category):
        return 2

    def delete_item(self, catgory, item):
        return

    @staticmethod
    def handle_delete_order(order_num):
        return "order is deleted"

    def send_file(self):
        return None

    def get_order(self, order_num) -> Order:
        return Order(OrderDetailBuilderFacade(), "0", 0.0)

    def get_correspond_menu(self) -> str:
        return "the corresponded menu"


@mock.patch('client.UpdateOrderMediator.set_item', new=OtherClass.set_item)
@mock.patch('client.UpdateOrderMediator.get_length', new=OtherClass.get_length)
@mock.patch("client.get_num", return_value=None)
@mock.patch("client.get_component", return_value=None)
@mock.patch("client.get_value", return_value=None)
def test_perform_action_update(get_value, get_component, get_num):
    inputs = []
    set_keyboard_input(inputs)
    update_processor = UpdateOrderMediator()
    perform_action("pizza", "update", update_processor)
    assert [] == get_display_output()


@mock.patch('client.UpdateOrderMediator.delete_item',
            new=OtherClass.delete_item)
@mock.patch('client.UpdateOrderMediator.get_length', new=OtherClass.get_length)
@mock.patch("client.get_num", return_value=None)
@mock.patch("client.get_component", return_value=None)
@mock.patch("client.get_value", return_value=None)
def test_perform_action_delete(get_value, get_component, get_num):
    inputs = []
    set_keyboard_input(inputs)
    update_processor = UpdateOrderMediator()
    perform_action("pizza", "delete", update_processor)
    assert [] == get_display_output()


@mock.patch('client.UpdateOrderMediator.get_length', new=OtherClass.get_length)
@mock.patch("client.create_pizza_order", return_value=None)
@mock.patch("client.get_component", return_value=None)
@mock.patch("client.create_drink_order", return_value=None)
def test_perform_action_add_pizza(get_value, get_component, get_num):
    inputs = []
    set_keyboard_input(inputs)
    update_processor = UpdateOrderMediator()
    with mock.patch.object(update_processor, 'order', OrderClass()):
        perform_action("pizza", "add", update_processor)
        assert [] == get_display_output()


@mock.patch('client.UpdateOrderMediator.get_length', new=OtherClass.get_length)
@mock.patch("client.create_pizza_order", return_value=None)
@mock.patch("client.get_component", return_value=None)
@mock.patch("client.create_drink_order", return_value=None)
def test_perform_action_add_drink(get_value, get_component, get_num):
    inputs = []
    set_keyboard_input(inputs)
    update_processor = UpdateOrderMediator()
    with mock.patch.object(update_processor, 'order', OrderClass()):
        perform_action("drink", "add", update_processor)
        assert [] == get_display_output()


@mock.patch('client.DeleteOrderMediator.handle_delete_order',
            new=OtherClass.handle_delete_order)
def test_delete_order():
    inputs = ["0", "q"]
    set_keyboard_input(inputs)
    delete_order()
    assert ["order is deleted"] == get_display_output()


@mock.patch('client.DeliveryMediator.get_order', new=OtherClass().get_order)
@mock.patch('client.DeliveryMediator.send_file', new=OtherClass().send_file)
@mock.patch("client.get_component", return_value=None)
@mock.patch("client.create_drink_order", return_value=None)
def test_ask_delivery(get_value, get_component):
    inputs = ["0", "foodora", "11 Wellesley"]
    set_keyboard_input(inputs)
    ask_for_delivery()
    assert [] == get_display_output()


@mock.patch("client.update_order", return_value=None)
def test_restaurant_operations_update(update_order):
    inputs = ["hahaha", "update_order", "q"]
    set_keyboard_input(inputs)
    restaurant_operation()
    assert [] == get_display_output()


@mock.patch("client.delete_order", return_value=None)
def test_restaurant_operations_delete(delete_order):
    inputs = ["hahaha", "delete order", "q"]
    set_keyboard_input(inputs)
    restaurant_operation()
    assert [] == get_display_output()


@mock.patch("client.create_new_order", return_value=None)
def test_restaurant_operations_create(delete_order):
    inputs = ["hahaha", "create order", "q"]
    set_keyboard_input(inputs)
    restaurant_operation()
    assert [] == get_display_output()


@mock.patch("client.view_menu", return_value=None)
def test_restaurant_operations_view_menu(delete_order):
    inputs = ["hahaha", "view menu", "q"]
    set_keyboard_input(inputs)
    restaurant_operation()
    assert [] == get_display_output()


@mock.patch('client.MenuMediator.get_correspond_menu',
            new=OtherClass().get_correspond_menu)
def test_view_menu_full():
    inputs = ["f"]
    set_keyboard_input(inputs)
    view_menu()
    assert ['the corresponded menu'] == get_display_output()


@mock.patch('client.MenuMediator.get_correspond_menu',
            new=OtherClass().get_correspond_menu)
def test_view_menu_item():
    inputs = ["i", "pizza", "pepperoni"]
    set_keyboard_input(inputs)
    view_menu()
    assert ['the corresponded menu'] == get_display_output()


if __name__ == '__main__':
    pytest.main(["client_test.py"])
