import runpy

from calculator.cli import handle_line, main


def run_session(monkeypatch, capsys, lines):
    """Feed lines to input(); running out of lines raises EOFError."""
    responses = iter(lines)

    def fake_input(prompt=""):
        try:
            return next(responses)
        except StopIteration:
            raise EOFError

    monkeypatch.setattr("builtins.input", fake_input)
    main()
    return capsys.readouterr().out


def test_each_operation_prints_its_answer(monkeypatch, capsys):
    lines = ["add 5 3", "subtract 5 3", "multiply 5 3", "divide 6 3", "exit"]
    output = run_session(monkeypatch, capsys, lines)
    assert "8.0" in output
    assert "2.0" in output
    assert "15.0" in output


def test_decimals_and_negative_numbers(monkeypatch, capsys):
    output = run_session(monkeypatch, capsys, ["add -2.5 1.5", "exit"])
    assert "-1.0" in output


def test_history_lists_successful_calculations_in_order(monkeypatch, capsys):
    lines = ["add 5 3", "multiply 2 4", "history", "exit"]
    output = run_session(monkeypatch, capsys, lines)
    assert "1. add 5 3 = 8.0" in output
    assert "2. multiply 2 4 = 8.0" in output


def test_history_when_empty(monkeypatch, capsys):
    output = run_session(monkeypatch, capsys, ["history", "exit"])
    assert "History is empty." in output


def test_history_remembers_across_lines_and_ignores_failures(monkeypatch, capsys):
    lines = ["add 1 1", "divide 1 0", "add x 1", "history", "exit"]
    output = run_session(monkeypatch, capsys, lines)
    assert "1. add 1 1 = 2.0" in output
    assert "2. " not in output


def test_history_rejects_extra_words(monkeypatch, capsys):
    output = run_session(monkeypatch, capsys, ["history now", "exit"])
    assert "history takes no numbers" in output


def test_divide_by_zero_shows_a_message_and_keeps_running(monkeypatch, capsys):
    lines = ["divide 1 0", "add 1 2", "exit"]
    output = run_session(monkeypatch, capsys, lines)
    assert "Cannot divide by zero" in output
    assert "3.0" in output


def test_unknown_command_is_reported(monkeypatch, capsys):
    output = run_session(monkeypatch, capsys, ["banana 1 2", "add 1 2", "exit"])
    assert "Unknown command: banana" in output
    assert "3.0" in output


def test_too_few_and_too_many_operands_are_reported(monkeypatch, capsys):
    lines = ["add 5", "add", "add 1 2 3", "exit"]
    output = run_session(monkeypatch, capsys, lines)
    assert "needs exactly 2 numbers, but got 1" in output
    assert "needs exactly 2 numbers, but got 0" in output
    assert "needs exactly 2 numbers, but got 3" in output


def test_invalid_numbers_are_reported(monkeypatch, capsys):
    output = run_session(monkeypatch, capsys, ["add a b", "add 1,5 2", "exit"])
    assert output.count("Invalid number") == 2


def test_blank_lines_are_skipped(monkeypatch, capsys):
    output = run_session(monkeypatch, capsys, ["", "   ", "add 1 2", "exit"])
    assert "3.0" in output
    assert "Unknown" not in output


def test_commands_are_case_insensitive(monkeypatch, capsys):
    output = run_session(monkeypatch, capsys, ["  ADD 1 2  ", "exit"])
    assert "3.0" in output


def test_exit_says_goodbye(monkeypatch, capsys):
    output = run_session(monkeypatch, capsys, ["exit"])
    assert "Goodbye!" in output


def test_end_of_input_ends_cleanly(monkeypatch, capsys):
    output = run_session(monkeypatch, capsys, ["add 1 2"])
    assert "3.0" in output
    assert "Goodbye!" in output


def test_end_of_input_with_no_lines_at_all(monkeypatch, capsys):
    output = run_session(monkeypatch, capsys, [])
    assert "Goodbye!" in output


def test_handle_line_returns_text_without_printing(capsys):
    history = []
    assert handle_line("add 5 3", history) == ["8.0"]
    assert capsys.readouterr().out == ""
    assert history == ["add 5 3 = 8.0"]


def test_entry_point_module_loads_without_starting_the_app(monkeypatch, capsys):
    def fail_if_called(prompt=""):
        raise AssertionError("input should not be called")

    monkeypatch.setattr("builtins.input", fail_if_called)
    runpy.run_module("calculator", run_name="imported")
    assert capsys.readouterr().out == ""


def test_each_answer_appears_as_its_own_exact_line(monkeypatch, capsys):
    lines = ["add 5 3", "subtract 5 3", "multiply 5 3", "divide 6 3", "exit"]
    output = run_session(monkeypatch, capsys, lines).splitlines()
    assert "8.0" in output
    assert "2.0" in output
    assert "15.0" in output
    assert output.count("2.0") == 2
