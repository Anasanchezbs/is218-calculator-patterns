from calculator.calculation import ArithmeticCalculation
from calculator.commands import CalculateCommand, HistoryCommand
from calculator.operations import Operations

# The strategy table: the command word picks the function.
OPERATIONS = {
    "add": Operations.add,
    "subtract": Operations.subtract,
    "multiply": Operations.multiply,
    "divide": Operations.divide,
}


def handle_line(line: str, history: list[str]) -> list[str]:
    """Process one typed line and return the lines to print."""
    parts = line.split()
    if not parts:
        return []
    name = parts[0].lower()
    operands = parts[1:]

    if name == "history":
        if operands:
            return ["history takes no numbers."]
        entries = HistoryCommand(history).execute()
        if not entries:
            return ["History is empty."]
        return [f"{number}. {entry}" for number, entry in enumerate(entries, 1)]

    if name not in OPERATIONS:
        return [
            f"Unknown command: {name}. "
            "Try add, subtract, multiply, divide, history, or exit."
        ]
    if len(operands) != 2:
        return [f"{name} needs exactly 2 numbers, but got {len(operands)}."]

    try:
        a = float(operands[0])
        b = float(operands[1])
    except ValueError:
        return ["Invalid number. Please enter numbers like 5 or -2.5."]

    calculation = ArithmeticCalculation.create(a, b, OPERATIONS[name])
    label = f"{name} {operands[0]} {operands[1]}"
    try:
        result = CalculateCommand(calculation, history, label).execute()
    except ValueError as error:
        return [f"Error: {error}"]
    return [str(result)]


def main() -> None:
    # Created once, outside the loop, so it remembers earlier work.
    history: list[str] = []
    print("Calculator ready. Commands: add, subtract, multiply, divide, history, exit")
    while True:
        try:
            line = input("> ")
        except EOFError:
            print("Goodbye!")
            break
        if line.strip().lower() == "exit":
            print("Goodbye!")
            break
        for text in handle_line(line, history):
            print(text)
