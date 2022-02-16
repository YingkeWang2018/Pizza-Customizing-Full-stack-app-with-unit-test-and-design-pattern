import pytest

from order_builder import *


# Class OrderDetailBuilderFacade
def test_order_detail_builder_facade_create_new_pizza():
    builder = OrderDetailBuilderFacade()
    pizza = builder.create_new_pizza()
    assert pizza.type is None
    assert pizza.quantity == 0
    assert pizza.size is None
    assert pizza.toppings == []


def test_order_detail_builder_facade_create_new_drink():
    builder = OrderDetailBuilderFacade()
    drink = builder.create_new_drink()
    assert drink.type is None
    assert drink.quantity == 0


def test_order_detail_builder_facade_add_pizza_to_order():
    builder = OrderDetailBuilderFacade()
    pizza = Pizza()
    builder.add_pizza_to_order(pizza)
    assert builder.pizza_order_builder.items[0] == pizza


def test_order_detail_builder_facade_add_drink_to_order():
    builder = OrderDetailBuilderFacade()
    drink = Drink()
    builder.add_drink_to_order(drink)
    assert builder.drink_order_builder.items[0] == drink


def test_order_detail_builder_facade_build_order_detail():
    builder = OrderDetailBuilderFacade()
    pizza = builder.create_new_pizza()
    drink = builder.create_new_drink()
    builder.add_pizza_to_order(pizza)
    builder.add_drink_to_order(drink)
    detail = builder.build_order_detail()
    assert detail["pizza"] == [{"type": None,
                                "size": None,
                                "toppings": [],
                                "quantity": 0
                                }]
    assert detail["drink"] == [{"name": None,
                                "quantity": 0}]


def test_order_detail_builder_facade_build_from_json():
    detail = {"pizza": [{"type": "blank",
                         "size": "s",
                         "toppings": ["beef"],
                         "quantity": 2
                         }],
              "drink": [{"name": "coke",
                         "quantity": 1}]}
    builder = OrderDetailBuilderFacade()
    builder.build_from_json(detail)
    pizza = builder.pizza_order_builder.items[0]
    drink = builder.drink_order_builder.items[0]
    assert pizza.type == "blank"
    assert pizza.quantity == 2
    assert pizza.size == "s"
    assert pizza.toppings == ["beef"]
    assert drink.type == "coke"
    assert drink.quantity == 1


def test_order_detail_builder_facade_build_order_detail_body_csv():
    builder = OrderDetailBuilderFacade()
    pizza = builder.create_new_pizza()
    pizza.type = "blank"
    pizza.size = "s"
    pizza.toppings = ["beef", "tomatoes"]
    pizza.quantity = 2
    drink = builder.create_new_drink()
    drink.type = "coke"
    drink.quantity = 1
    builder.add_pizza_to_order(pizza)
    builder.add_drink_to_order(drink)
    csv = builder.build_order_detail_body_csv()
    assert csv == [{
        "order_detail/category": "pizza",
        "order_detail/type": "blank",
        "order_detail/size": "s",
        "order_detail/toppings": ','.join(["beef", "tomatoes"]),
        "order_detail/quantity": 2
    }, {
        "order_detail/category": "drink",
        "order_detail/type": "coke",
        "order_detail/size": None,
        "order_detail/toppings": None,
        "order_detail/quantity": 1
    }]


def test_order_detail_builder_facade_build_order_detail_csv_header():
    builder = OrderDetailBuilderFacade()
    header = builder.build_order_detail_csv_header()
    assert header == ["order_detail/category",
                      "order_detail/type",
                      "order_detail/size",
                      "order_detail/toppings",
                      "order_detail/quantity"]


def test_order_detail_builder_facade_str():
    builder = OrderDetailBuilderFacade()
    pizza = builder.create_new_pizza()
    pizza.type = "margherita"
    pizza.size = "l"
    pizza.toppings = ["chicken"]
    pizza.quantity = 1
    builder.add_pizza_to_order(pizza)
    drink = builder.create_new_drink()
    drink.type = "dr. pepper"
    drink.quantity = 2
    builder.add_drink_to_order(drink)
    drink = builder.create_new_drink()
    drink.type = "pepsi"
    drink.quantity = 1
    builder.add_drink_to_order(drink)
    assert builder.__str__() == "Pizza(s):\nItem number 0: type: margherita, size: l, toppings: chicken, quantity: 1" \
                                "\nDrink(s):\nItem number 0: name: dr. pepper, quantity: 2\nItem number 1: name: pepsi, quantity: 1"


# Class OrderBuilder
def test_order_builder_add_item_to_order():
    builder = OrderBuilder()
    item = Item()
    builder.add_item_to_order(item)
    assert builder.items[0] == item


def test_order_builder_get_dict_representation():
    builder = OrderBuilder()
    pizza = Pizza()
    pizza.type = "blank"
    pizza.size = "s"
    pizza.toppings = ["beef"]
    pizza.quantity = 2
    builder.add_item_to_order(pizza)
    result = builder.get_dict_representation()
    assert result == [{
        "type": "blank",
        "size": "s",
        "toppings": ["beef"],
        "quantity": 2
    }]


def test_order_builder_get_csv_dict_represent():
    builder = OrderBuilder()
    drink = Drink()
    drink.type = "coke"
    drink.quantity = 1
    builder.add_item_to_order(drink)
    result = builder.get_csv_dict_represent()
    assert result == [{
        "order_detail/category": "drink",
        "order_detail/type": "coke",
        "order_detail/size": None,
        "order_detail/toppings": None,
        "order_detail/quantity": 1
    }]


def test_order_builder_str():
    builder = OrderBuilder()
    drink = Drink()
    drink.type = "coke"
    drink.quantity = 1
    builder.add_item_to_order(drink)
    assert builder.__str__() == "\nItem number 0: name: coke, quantity: 1"


# Class PizzaOrderBuilder
def test_pizza_order_builder_build_from_json():
    detail = [{"type": "blank",
               "size": "s",
               "toppings": ["beef"],
               "quantity": 2
               }]
    builder = PizzaOrderBuilder()
    builder.build_from_json(detail)
    assert builder.items[0].type == "blank"
    assert builder.items[0].size == "s"
    assert builder.items[0].toppings == ["beef"]
    assert builder.items[0].quantity == 2


def test_pizza_order_builder_create_new_pizza():
    builder = PizzaOrderBuilder()
    pizza = builder.create_new_pizza()
    assert pizza.type is None
    assert pizza.quantity == 0
    assert pizza.size is None
    assert pizza.toppings == []


# Class DrinkOrderBuilder
def test_drink_order_builder_build_from_json():
    detail = [{"name": "coke",
               "quantity": 1
               }]
    builder = DrinkOrderBuilder()
    builder.build_from_json(detail)
    assert builder.items[0].type == "coke"
    assert builder.items[0].quantity == 1


def test_drink_order_builder_create_new_pizza():
    builder = DrinkOrderBuilder()
    drink = builder.create_new_drink()
    assert drink.type is None
    assert drink.quantity == 0


# Class Item
def test_item_add_type():
    item = Item()
    item._add_type("coke")
    assert item.type == "coke"


def test_item_add_quantity():
    item = Item()
    item.add_quantity(1)
    assert item.quantity == 1


def test_item_build_from_json():
    detail = {"quantity": 3}
    item = Item()
    item.build_from_json(detail)
    assert item.quantity == 3


# Class Pizza
def test_pizza_add_pizza_type():
    pizza = Pizza()
    pizza.add_pizza_type("pepperoni")
    assert pizza.type == "pepperoni"


def test_pizza_set_size():
    pizza = Pizza()
    pizza.set_size("M") is True
    assert pizza.size == "M"


def test_pizza_add_toppings():
    pizza = Pizza()
    assert pizza.add_toppings("beef", ("olives",
                                       "tomatoes",
                                       "mushrooms",
                                       "jalapenos",
                                       "chicken",
                                       "beef",
                                       "pepperoni",
                                       "q"
                                       )) is True
    assert pizza.toppings == ["beef"]
    assert pizza.add_toppings("beef", ("olives",
                                       "tomatoes",
                                       "mushrooms",
                                       "jalapenos",
                                       "chicken",
                                       "beef",
                                       "pepperoni",
                                       "q"
                                       )) is False
    assert pizza.toppings == ["beef"]
    assert pizza.add_toppings("pork", ("olives",
                                       "tomatoes",
                                       "mushrooms",
                                       "jalapenos",
                                       "chicken",
                                       "beef",
                                       "pepperoni",
                                       "q"
                                       )) is False
    assert pizza.toppings == ["beef"]


def test_pizza_get_dict_represent():
    pizza = Pizza()
    pizza.type = "vegetarian"
    pizza.size = "L"
    pizza.toppings = ["chicken"]
    pizza.quantity = 1
    assert pizza.get_dict_represent() == {
        "type": "vegetarian",
        "size": "L",
        "toppings": ["chicken"],
        "quantity": 1
    }


def test_pizza_write_to_csv_dict():
    pizza = Pizza()
    pizza.type = "vegetarian"
    pizza.size = "L"
    pizza.toppings = ["chicken"]
    pizza.quantity = 1
    assert pizza.write_to_csv_dict() == {
        "order_detail/category": "pizza",
        "order_detail/type": "vegetarian",
        "order_detail/size": "L",
        "order_detail/toppings": ','.join(["chicken"]),
        "order_detail/quantity": 1
    }


def test_pizza_build_from_json():
    detail = {"type": "margherita",
              "size": "S",
              "toppings": [],
              "quantity": 2
              }
    pizza = Pizza()
    pizza.build_from_json(detail)
    assert pizza.quantity == 2
    assert pizza.type == "margherita"
    assert pizza.size == "S"
    assert pizza.toppings == []


def test_pizza_set_component():
    pizza = Pizza()
    pizza.set_component("type", "blank")
    pizza.set_component("size", "m")
    pizza.set_component("toppings", ["chicken"])
    pizza.set_component("quantity", 1)
    assert pizza.type == "blank"
    assert pizza.size == "m"
    assert pizza.toppings == ["chicken"]
    assert pizza.quantity == 1


def test_pizza_str():
    pizza = Pizza()
    pizza.type = "blank"
    pizza.size = "l"
    pizza.toppings = ["tomatoes", "chicken"]
    pizza.quantity = 2
    assert pizza.__str__() == "type: blank, size: l, toppings: tomatoes,chicken, quantity: 2"


# Class Drink
def test_drink_write_to_csv_dict():
    drink = Drink()
    drink.type = "diet pepsi"
    drink.quantity = 3
    assert drink.write_to_csv_dict() == {
        "order_detail/category": "drink",
        "order_detail/type": "diet pepsi",
        "order_detail/size": None,
        "order_detail/toppings": None,
        "order_detail/quantity": 3
    }


def test_drink_add_drink_type():
    drink = Drink()
    drink.add_drink_type("Water")
    assert drink.type == "Water"


def test_drink_get_dict_represent():
    drink = Drink()
    drink.type = "juice"
    drink.quantity = 1
    assert drink.get_dict_represent() == {"name": "juice",
                                          "quantity": 1}


def test_drink_build_from_json():
    detail = {"name": "pepsi",
              "quantity": 4
              }
    drink = Drink()
    drink.build_from_json(detail)
    assert drink.quantity == 4
    assert drink.type == "pepsi"


def test_drink_set_component():
    drink = Drink()
    drink.set_component("name", "coke")
    drink.set_component("quantity", 3)
    assert drink.type == "coke"
    assert drink.quantity == 3


def test_drink_str():
    drink = Drink()
    drink.type = "coke"
    drink.quantity = 2
    assert drink.__str__() == "name: coke, quantity: 2"


if __name__ == "__main__":
    pytest.main(['order_builder_test.py'])
