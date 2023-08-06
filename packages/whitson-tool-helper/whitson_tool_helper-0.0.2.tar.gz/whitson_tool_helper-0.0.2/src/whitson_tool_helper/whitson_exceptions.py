class WhitsonException(Exception):
    pass


class CalculationTimeoutError(WhitsonException):
    def __str__(self) -> str:
        return "Calculation timed out. Please contact the support team."
