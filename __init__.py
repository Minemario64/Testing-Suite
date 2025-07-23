from rich import traceback ; traceback.install()
from typing import Callable, NamedTuple, Iterator
from rich.console import Console
from utils import *
from draw import *
import re
from shutil import get_terminal_size

cli = Console(highlight=False)
CLEAR: str = "\033[2J\033[H"

class TestResults(NamedTuple):
    description: str
    result: bool | None

def printFeatureStyled(description: str, tests: list[TestResults] | None) -> None:
    COLOR: str = "sea_green2"
    TERMINAL_WIDTH = get_terminal_size().columns

    rectangle: list[str] | str = rect(max(([len(test.description) for test in tests] if not tests is None else []) + [len(description)]) + 8, 5 if tests is None else 4 + (len(tests) * 5), lengthMultiplier=1).split("\n")
    rectangle[1] = f"{RECT_CHARS[EDGE_X]}{" "*3}[bold]{description}[/bold]{" "*3}{RECT_CHARS[EDGE_X]}"
    rectangle[2] = f"├{"─"*(len(rectangle[2]) - 2)}┤"

    rectangle = f"[{COLOR}]{centerStr("\n".join(rectangle), TERMINAL_WIDTH, styled=True)}[/{COLOR}]"

    cli.print(CLEAR + rectangle)

def it(testDescription: str, codePlusExpectations: str) -> TestResults:

    def process(funcStr: str) -> str:
        lns = funcStr.split("\n")
        for i, ln in enumerate(lns):
            passedPattern = re.compile(r" *passed\(.*\)")
            if passedPattern.match(ln):
                lns[i] = f"{" "*countUntilLand(ln)}if not passed({ln.lstrip(" ").removeprefix("passed(").removesuffix(")")}): return False"

        lns.append(f"{" "*countUntilLand(lns[1])}return True")
        return "\n".join(lns)

    testStr: str = f"def test() -> bool:\n    {"\n    ".join([ln for ln in codePlusExpectations.split("\n") if ln != ""])}"
    testStr = process(testStr)
    scope: dict = globals()
    exec(testStr, scope)
    return TestResults(testDescription, scope["test"]())

def describe(featureDescription: str, tests: str) -> None:
    printFeatureStyled(featureDescription, None)

    def process(funcStr: str) -> str:
        lns = funcStr.split("\n")
        for i, ln in enumerate(lns):
            passedPattern = re.compile(r" *it\(")
            matched = passedPattern.match(ln)
            if matched:
                text = f"{" "*countUntilLand(ln)}testResults.append(it({traverseFuncStr(funcStr, matched.pos + (len("\n".join(lns[0:i-1])) - 1))}))"
                for exi, chars in enumerate(text.split("\n"), 0):
                    lns[i + exi] = chars

                lns.insert(i + text.count("\n") + 1, f"{" "*countUntilLand(ln)}printFeatureStyled(featureDesc, testResults)")

        lns.append(f"{" "*countUntilLand(lns[1])}return True")
        return "\n".join(lns)

    testStrs: str = f"def testFeature() -> bool:\n    testResults: list[TestResults] = []\n    {"\n    ".join([ln for ln in tests.split("\n") if ln != ""])}\n    return not testResults.__contains__(False)"
    scope: dict = globals()
    scope["featureDesc"] = featureDescription
    exec(process(testStrs), scope)
    print(scope["testFeature"]())

passed: Callable[[bool], bool] = lambda passed: passed

if __name__ == "__main__":
    def add(a: int, b: int) -> int:
        return a + b

    describe("Basic Arithmetic", '''
it("Adds 2 numbers", """
    import time
    time.sleep(3)
    result = add(2, 2)
    passed(result == 4)
""")
''')