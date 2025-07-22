from rich import traceback ; traceback.install()
from typing import Callable

def it(testDescription: str, codePlusExpectations: Callable[[], bool]) -> None:
    codePlusExpectations()

def describe(featureDescription: str, tests: Callable[[], bool | None]) -> None:
    tests()

def add(a, b) -> int:
    return a + b

def check() -> bool:
    result = add(2, 2)
    if result == 4:
        return True

    return False

def funcHI():
    it("HI", check)

describe("H", it)