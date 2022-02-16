from typing import Optional

from requests.exceptions import ConnectionError

from data_keywords_loader import DataKeyWordsLoader
from exception import QuitError
from mediator import CreateOrderMediator, DeleteOrderMediator, DeliveryMediator, \
    MenuMediator, UpdateOrderMediator
from msg_constant import *

BASE = " http://127.0.0.1:5000/"
try:
    DataKeyWordsLoader.load_keywords()
except ConnectionError:
    pass
MAX_ORDER_QUANTITY = 50
UPDATE_ACTION_KEYWORDS = ("update", "delete", "add", "q")
RESTAURANT_OPERATIONS = (
    "update order", "delete order", "create order", "ask delivery", "view menu",
    'q')
MENU_CHOICE = ("f", "i", 'c', "q")


def check_quit(client_input: str) -> None:
    if client_input == 'q':
        raise QuitError


def create_single_pizza(create_order_processor: CreateOrderMediator) -> None:
    pizza = create_order_processor.get_temp_pizza()
    type_ = get_keyword(DataKeyWordsLoader.get_pizza_type_keys(),
                        CREATE_PIZZA_TYPE_MSG)
    pizza.add_pizza_type(type_)
    size = get_keyword(DataKeyWordsLoader.get_pizza_size_keys(),
                       CREATE_PIZZA_SIZE_MSG.format(
                           DataKeyWordsLoader.get_pizza_size_keys()))
    pizza.set_size(size)
    while True:
        topping = input(CREATE_PIZZA_TOPPING)
        check_quit(topping)
        if topping == 'e':
            break
        if not pizza.add_toppings(topping,
                                  DataKeyWordsLoader.get_pizza_topping_keys()):
            print("This topping is invalid")
    quantity = input("Enter the quantity (q for quitting creating) : ")
    while not create_order_processor.handle_item_quantity(quantity, "pizza"):
        quantity = input(
            "Invalid input! Enter the quantity (q for quitting creating) : ")
    create_order_processor.add_pizza_to_order()
    print("Finish pizza Creating!")


def create_single_drink(create_order_processor: CreateOrderMediator) -> None:
    drink = create_order_processor.get_temp_drink()
    drink_name = get_keyword(DataKeyWordsLoader.get_drink_name_keys(),
                             CREATE_DRINK_NAME_MSG)
    drink.add_drink_type(drink_name)
    quantity = input("Enter drink quantity (q for quitting): ")
    check_quit(quantity)
    while not create_order_processor.handle_item_quantity(quantity, "drink"):
        quantity = input(
            "Invalid input! Enter the quantity (q for quitting creating) : ")
    create_order_processor.add_drink_to_order()
    print("Finish drink Creating!")


def create_drink_order(create_order_processor: CreateOrderMediator) -> None:
    while True:
        answer = input(
            "Do you Want to Order a Drink? (Y for yes otherwise is a no): ")
        if answer != 'Y':
            print("Thank you for ordering drinks!")
            return
        try:
            create_single_drink(create_order_processor)
        except QuitError:
            pass


def create_pizza_order(create_order_processor: CreateOrderMediator) -> Optional[
    list]:
    while True:
        answer = input(
            "Do you Want to Order a Pizza? (Y for yes otherwise is a no): ")
        if answer != 'Y':
            print("Thank you for ordering pizzas!")
            return
        try:
            create_single_pizza(create_order_processor)
        except QuitError:
            pass


def create_new_order():
    print("Create a New Order")
    create_order_processor = CreateOrderMediator()
    create_pizza_order(create_order_processor)
    create_drink_order(create_order_processor)
    print(create_order_processor.build_order_detail())


def get_no_option_input(msg: str):
    order_num = ''
    while not order_num:
        order_num = input(msg).strip()
        check_quit(order_num)
    return order_num


def get_keyword(keywords, msg):
    response = input(msg).strip().lower()
    check_quit(response)
    while response not in keywords:
        response = input("Unreadable input! " + msg)
        check_quit(response)
    return response


def get_num(length, msg):
    while True:
        num = input(msg).strip().lower()
        if num == 'q' or (num.isnumeric() and 0 <= int(num) < length):
            check_quit(num)
            return int(num)


def get_component(category):
    if category == 'pizza':
        components = DataKeyWordsLoader.get_pizza_component_keys()
    else:
        components = DataKeyWordsLoader.get_drink_component_keys()
    return get_keyword(components, GET_COMPONENT_MSG)


def get_toppings():
    while True:
        toppings = input(GET_TOPPINGS_MSG).strip().lower()
        check_quit(toppings)
        all_valid = True
        topping_lst = toppings.split()
        for t in topping_lst:
            if t not in DataKeyWordsLoader.get_pizza_topping_keys():
                all_valid = False
        if all_valid:
            return topping_lst


def get_value(component):
    value = None
    msg = GET_VALUE_MSG.format(component)
    if component == 'type':
        value = get_keyword(DataKeyWordsLoader.get_pizza_type_keys(), msg)
    elif component == 'size':
        value = get_keyword(DataKeyWordsLoader.get_pizza_size_keys(), msg)
    elif component == 'toppings':
        value = get_toppings()
    elif component == 'name':
        value = get_keyword(DataKeyWordsLoader.get_drink_name_keys(), msg)
    elif component == 'quantity':
        value = get_num(MAX_ORDER_QUANTITY, msg)
    return value


def perform_action(category, action, update_mediator):
    if action == 'update':
        item_num = get_num(update_mediator.get_length(category),
                           GET_ITEM_NUM_MSG)
        component = get_component(category)
        value = get_value(component)
        update_mediator.set_item(category, item_num, component, value)
    elif action == 'delete':
        item_num = get_num(update_mediator.get_length(category),
                           GET_ITEM_NUM_MSG)
        update_mediator.delete_item(category, item_num)
    elif action == 'add':
        create_mediator = CreateOrderMediator()
        create_mediator.order_detail = update_mediator.order.order_detail
        if category == 'pizza':
            create_pizza_order(create_mediator)
        elif category == 'drink':
            create_drink_order(create_mediator)


def update_order():
    order_num = None
    update_mediator = UpdateOrderMediator()
    try:
        while update_mediator.order is None:
            order_num = get_no_option_input(GET_ORDER_NUM_UPDATE_MSG)
            update_mediator.get_order(order_num)
        print(update_mediator)
        category = get_keyword(DataKeyWordsLoader.get_category_keys(),
                               GET_CATEGORY_MSG)
        action = get_keyword(UPDATE_ACTION_KEYWORDS, GET_ACTION_MSG)
        perform_action(category, action, update_mediator)
    except QuitError:
        return
    update_mediator.set_order(order_num)
    print(update_mediator)


def delete_order():
    try:
        while True:
            order_num = get_no_option_input(GET_ORDER_NUM_DELETE_MSG)
            print(DeleteOrderMediator.handle_delete_order(order_num))
    except QuitError:
        return


def ask_for_delivery():
    try:
        delivery_handler = DeliveryMediator()
        order = None
        while order is None:
            order_num = get_no_option_input(GET_ORDER_NUM_DELIVERY_MSG)
            order = delivery_handler.get_order(order_num)
        service = ''

        while not order.set_service(service):
            service = get_no_option_input(GET_SERVICE_MSG)

        if order.need_address():
            address = ''
            while not order.set_address(address):
                address = get_no_option_input(GET_ADDRESS_MSG)
        delivery_handler.send_file()
    except QuitError:
        return


def view_menu() -> None:
    try:
        menu_processor = MenuMediator()
        menu_type = get_keyword(MENU_CHOICE, MENU_TYPE_MSG)
        if menu_type == 'f':
            pass
        elif menu_type == 'c' or 'i':
            category_type = get_keyword(
                DataKeyWordsLoader.get_menu_category_keys(),
                GET_MENU_CATEGORY_MSG.format(
                    DataKeyWordsLoader.get_category_keys()))
            menu_processor.set_category(category_type)
            if menu_type == 'i':
                item_type = get_keyword(
                    menu_processor.get_correspond_item_keys(),
                    GET_ITEM_MSG_UNDER_CAT)
                menu_processor.set_item(item_type)
        print(menu_processor.get_correspond_menu())

    except QuitError:
        pass


def restaurant_operation() -> None:
    while True:
        try:
            operation = get_no_option_input(
                GET_RESTAURANT_OPERATION_MSG).lower()
            while operation not in RESTAURANT_OPERATIONS:
                operation = get_no_option_input(
                    GET_RESTAURANT_OPERATION_MSG).lower()
            if operation == "update order":
                update_order()
            elif operation == "delete order":
                delete_order()
            elif operation == "create order":
                create_new_order()
            elif operation == "view menu":
                view_menu()
            elif operation == "ask delivery":
                ask_for_delivery()
        except QuitError:
            return


if __name__ == '__main__':
    restaurant_operation()
