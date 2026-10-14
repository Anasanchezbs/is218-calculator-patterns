import pytest

from calculator.operations import Operations


def test_add_positive_numbers():
    assert Operations.add(5, 3) == 8


def test_add_negative_and_decimal_numbers():
    assert Operations.add(-4, 1.5) == -2.5


def test_subtract():
    assert Operations.subtract(5, 3) == 2


def test_subtract_can_give_a_negative_result():
    assert Operations.subtract(3, 10) == -7


def test_multiply():
    assert Operations.multiply(5, 3) == 15


def test_multiply_negative_and_decimal_numbers():
    assert Operations.multiply(-2, 1.5) == -3


def test_divide():
    assert Operations.divide(6, 3) == 2


def test_divide_with_a_decimal_result():
    assert Operations.divide(7, 2) == 3.5


def test_divide_by_zero_raises_value_error_with_message():
    with pytest.raises(ValueError, match="Cannot divide by zero"):
        Operations.divide(1, 0)


def test_divide_zero_by_a_number_is_allowed():
    assert Operations.divide(0, 5) == 0


def test_operations_with_zero():
    assert Operations.add(0, 5) == 5
    assert Operations.add(5, 0) == 5
    assert Operations.subtract(5, 0) == 5
    assert Operations.subtract(0, 5) == -5
    assert Operations.multiply(0, 5) == 0
    assert Operations.multiply(5, 0) == 0
