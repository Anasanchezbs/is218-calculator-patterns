from calculator.calculation import Calculation


class CalculateCommand:
    def __init__(
        self,
        calculation: Calculation,
        history: list[str],
        label: str = "calculation",
    ):
        # The command receives its pieces instead of building them.
        self.calculation = calculation
        self.history = history
        self.label = label

    def execute(self) -> float:
        # If execute() raises, the next line never runs, so history is unchanged.
        result = self.calculation.execute()
        self.history.append(f"{self.label} = {result}")
        return result


class HistoryCommand:
    def __init__(self, history: list[str]):
        self.history = history

    def execute(self) -> list[str]:
        # A copy: the caller cannot change the stored list.
        return self.history.copy()
