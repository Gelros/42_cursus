from abc import ABC, abstractmethod
from typing import Any, List


class DataProcessor(ABC):
    @abstractmethod
    def process(self, data: Any) -> str:
        pass

    @abstractmethod
    def validate(self, data: Any) -> bool:
        pass

    def format_output(self, result: str) -> str:
        return f"{result}"


class NumericProcessor(DataProcessor):
    def __init__(self) -> None:
        self.name = "Numeric Processor"

    def validate(self, data: List) -> bool:
        d = data
        valid = isinstance(data, list) and all(isinstance(x, (int)) for x in d)
        return valid

    def process(self, data: List) -> str:
        if not self.validate(data):
            raise ValueError("Invalid numeric data")
        som = sum(x for x in data)
        len_d = len(data)
        avg = som / len_d
        res = f"Processed {len_d} numeric values, sum={som}, avg={avg:.1f}"
        return self.format_output(res)

    def validation(self, data: str) -> str:
        if self.validate(data):
            return "Validation: Numeric data verified"


class TextProcessor(DataProcessor):
    def __init__(self) -> None:
        self.name = "Text Processor"

    def validate(self, data: str) -> bool:
        return isinstance(data, str)

    def process(self, data: str) -> str:
        if not self.validate(data):
            raise ValueError("Invalid str data")
        len_str = len(data)
        count_word = len(data.split())
        res = f"Processed text: {len_str} characters, {count_word} words"
        return self.format_output(res)

    def validation(self, data: str) -> str:
        if self.validate(data):
            return "Validation: Text data verified"


class LogProcessor(DataProcessor):
    def __init__(self) -> None:
        self.name = "Log Processor..."

    def validate(self, data: str) -> bool:
        return isinstance(data, str)

    def process(self, data: str) -> str:
        if not self.validate(data):
            raise ValueError("Invalid str data")
        type_mess, message = data.split(':', 1)
        res = f"[ALERT] {type_mess} level detected:{message}"
        return self.format_output(res)

    def validation(self, data: str) -> str:
        if self.validate(data):
            return "Validation: Log entry verified"


def main() -> None:
    print("=== CODE NEXUS - DATA PROCESSOR FOUNDATION ===")
    num, text, log = NumericProcessor(), TextProcessor(), LogProcessor()
    data_num, data_text = [1, 4, 3], "Hello Nexus World"
    data_log = "ERROR: Connection timeout"

    processors: List[DataProcessor] = [num, text, log]
    test_data: List[Any] = [data_num, data_text, data_log]

    for p, data in zip(processors, test_data):
        try:
            print()
            print(f"Initializing {p.name}...")
            print(f"Processing data: {data}")
            print(p.validation(data))
            print(f"Output: {p.process(data)}")
        except Exception as e:
            print(f"Output: {e}")

    print()
    print("=== Polymorphic Processing Demo ===")
    print("Processing multiple data types through same interface...")
    i = 0
    for p, data in zip(processors, test_data):
        i = i + 1
        print(f"Result {i}: {p.process(data)}")
    print()
    print("Foundation systems online. Nexus ready for advanced streams.")


if __name__ == "__main__":
    main()
