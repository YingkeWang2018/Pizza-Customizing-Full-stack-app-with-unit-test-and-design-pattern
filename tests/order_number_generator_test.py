import pytest

from order_number_generator import *


# order_number_generator.py
def test_order_number_generator_get_random_string():
    result = get_random_string()
    assert result.islower() is True
    assert result.isalpha() is True
    assert len(result) == 8


if __name__ == "__main__":
    pytest.main(['order_number_generator_test.py'])
