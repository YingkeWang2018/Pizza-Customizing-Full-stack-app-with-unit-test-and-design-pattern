from typing import Tuple

import requests

BASE = " http://127.0.0.1:5000/"


class DataKeyWordsLoader:
    _category_keys = None
    _pizza_component_keys = None
    _pizza_topping_keys = None
    _drink_component_keys = None
    _pizza_type_keys = None
    _pizza_size_keys = None
    _drink_name_keys = None
    _menu_category_keys = None

    @staticmethod
    def get_category_keys() -> Tuple[str]:
        return DataKeyWordsLoader._category_keys

    @staticmethod
    def load_keywords() -> None:
        load_dict = requests.get(BASE + "/keywords").json()
        DataKeyWordsLoader._category_keys = tuple(
            load_dict["CATEGORY_KEYWORDS"])
        DataKeyWordsLoader._pizza_size_keys = tuple(
            load_dict["PIZZA_SIZE_KEYWORDS"])
        DataKeyWordsLoader._drink_component_keys = tuple(
            load_dict["DRINK_COMPONENTS_KEYWORDS"])
        DataKeyWordsLoader._pizza_component_keys = tuple(
            load_dict["PIZZA_COMPONENTS_KEYWORDS"])
        DataKeyWordsLoader._pizza_topping_keys = tuple(
            load_dict["PIZZA_TOPPING_KEYWORDS"])
        DataKeyWordsLoader._drink_name_keys = tuple(
            load_dict["DRINK_NAME_KEYWORDS"])
        DataKeyWordsLoader._pizza_type_keys = tuple(
            load_dict["PIZZA_TYPE_KEYWORDS"])
        DataKeyWordsLoader._menu_category_keys = tuple(
            load_dict["MENU_CATEGORY_KEYWORDS"])

    @staticmethod
    def get_pizza_component_keys() -> Tuple[str]:
        return DataKeyWordsLoader._pizza_component_keys

    @staticmethod
    def get_drink_component_keys() -> Tuple[str]:
        return DataKeyWordsLoader._drink_component_keys

    @staticmethod
    def get_pizza_type_keys() -> Tuple[str]:
        return DataKeyWordsLoader._pizza_type_keys

    @staticmethod
    def get_pizza_size_keys() -> Tuple[str]:
        return DataKeyWordsLoader._pizza_size_keys

    @staticmethod
    def get_pizza_topping_keys() -> Tuple[str]:
        return DataKeyWordsLoader._pizza_topping_keys

    @staticmethod
    def get_drink_name_keys() -> Tuple[str]:
        return DataKeyWordsLoader._drink_name_keys

    @staticmethod
    def get_menu_category_keys() -> Tuple[str]:
        return DataKeyWordsLoader._menu_category_keys
