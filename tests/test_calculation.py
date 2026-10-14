import pytest

from calculator.calculation import ArithmeticCalculation, Calculation
from calculator.operations import Operations


def test_create_returns_an_arithmetic_calculation():
    calculation = ArithmeticCalculation.create(5, 3, Operations.add)
    assert isinstance(calculation, ArithmeticCalculation)


def test_calculation_stores_its_numbers_and_operation():
    calculation = ArithmeticCalculation.create(5, 3, Operations.subtract)
    assert calculation.a == 5
    assert calculation.b == 3
    assert calculation.operation is Operations.subtract


def test_creating_a_calculation_does_not_run_it():
    calls = []

    def spy(a, b):
        calls.append((a, b))
        return a + b

    calculation = ArithmeticCalculation.create(1, 2, spy)
    assert calls == []
    assert calculation.execute() == 3
    assert calls == [(1, 2)]


def test_execute_runs_each_operation():
    cases = [
        (Operations.add, 8),
        (Operations.subtract, 2),
        (Operations.multiply, 15),
        (Operations.divide, 5 / 3),
    ]
    for operation, expected in cases:
        calculation = ArithmeticCalculation.create(5, 3, operation)
        assert calculation.execute() == pytest.approx(expected)


def test_execute_with_decimals_and_negatives():
    calculation = ArithmeticCalculation.create(-2.5, 4, Operations.multiply)
    assert calculation.execute() == -10


def test_division_by_zero_fails_when_executed_not_when_created():
    calculation = ArithmeticCalculation.create(1, 0, Operations.divide)
    with pytest.raises(ValueError, match="Cannot divide by zero"):
        calculation.execute()


def test_the_abstract_calculation_cannot_be_created():
    with pytest.raises(TypeError):
        Calculation.create(5, 3, Operations.add)


def test_a_subclass_without_execute_cannot_be_created():
    class Incomplete(Calculation):
        pass

    with pytest.raises(TypeError):
        Incomplete.create(1, 2, Operations.add)


def test_create_builds_the_class_that_called_it():
    class Doubling(Calculation):
        def execute(self):
            return self.operation(self.a, self.b) * 2

    calculation = Doubling.create(1, 2, Operations.add)
    assert isinstance(calculation, Doubling)
    assert calculation.execute() == 6


def test_two_calculations_are_independent():
    first = ArithmeticCalculation.create(1, 1, Operations.add)
    second = ArithmeticCalculation.create(10, 10, Operations.add)
    assert first.execute() == 2
    assert second.execute() == 20
