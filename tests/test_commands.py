import pytest

from calculator.calculation import ArithmeticCalculation
from calculator.commands import CalculateCommand, HistoryCommand
from calculator.operations import Operations


def make(a, b, operation):
    return ArithmeticCalculation.create(a, b, operation)


def test_calculate_command_returns_the_answer_and_records_an_entry():
    history = []
    command = CalculateCommand(make(5, 3, Operations.add), history, "add 5 3")
    assert command.execute() == 8
    assert history == ["add 5 3 = 8"]


def test_entry_uses_the_label_when_given():
    history = []
    CalculateCommand(make(6, 3, Operations.divide), history, "divide 6 3").execute()
    assert history == ["divide 6 3 = 2.0"]


def test_creating_the_command_does_not_run_the_calculation():
    history = []
    CalculateCommand(make(5, 3, Operations.add), history, "add 5 3")
    assert history == []


def test_failed_calculation_leaves_history_unchanged():
    history = ["add 1 1 = 2"]
    command = CalculateCommand(make(1, 0, Operations.divide), history, "divide 1 0")
    with pytest.raises(ValueError, match="Cannot divide by zero"):
        command.execute()
    assert history == ["add 1 1 = 2"]


def test_a_success_after_a_failure_is_still_recorded():
    history = []
    bad = CalculateCommand(make(1, 0, Operations.divide), history, "divide 1 0")
    with pytest.raises(ValueError):
        bad.execute()
    CalculateCommand(make(2, 2, Operations.add), history, "add 2 2").execute()
    assert history == ["add 2 2 = 4"]


def test_history_command_returns_entries_in_order():
    history = []
    CalculateCommand(make(1, 1, Operations.add), history, "add 1 1").execute()
    CalculateCommand(make(5, 3, Operations.subtract), history, "subtract 5 3").execute()
    assert HistoryCommand(history).execute() == [
        "add 1 1 = 2",
        "subtract 5 3 = 2",
    ]


def test_history_command_on_an_empty_history():
    assert HistoryCommand([]).execute() == []


def test_changing_the_returned_list_cannot_change_the_history():
    history = ["add 1 1 = 2"]
    returned = HistoryCommand(history).execute()
    returned.append("bogus")
    returned.clear()
    assert history == ["add 1 1 = 2"]


def test_both_commands_share_the_same_history_list():
    history = []
    CalculateCommand(make(1, 1, Operations.add), history, "add 1 1").execute()
    assert HistoryCommand(history).execute() == ["add 1 1 = 2"]
    CalculateCommand(make(2, 2, Operations.add), history, "add 2 2").execute()
    assert len(HistoryCommand(history).execute()) == 2


def test_the_default_label_is_used_when_none_is_given():
    history = []
    CalculateCommand(make(1, 2, Operations.add), history).execute()
    assert history == ["calculation = 3"]
