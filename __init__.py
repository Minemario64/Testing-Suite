from typing import Any, Iterator
from rich.console import Console

con = Console(highlight=False)

class Equation:

    def __init__(self, func: callable) -> None:
        self.func = func

    def check(self, *args, **kwargs) -> bool:
        val = self.func(*args, **kwargs)
        if not isinstance(val, bool):
            raise ValueError(f"Function: {self.func.__name__} did not return a boolean.")

        return val

class Test:

    def __init__(self, name: str, desc: str) -> None:
        self.name = name
        self.desc = desc

    def run(self, Handling: bool = True, styling: bool = True) -> None | bool:
        raise NotImplementedError("Cannot run the base test")

class UnitTest(Test):

    def __init__(self, name: str, desc: str, func: callable, *args, **kwargs) -> None:
        super().__init__(name if name != "" else func.name, desc)
        self.func: callable = func
        self.args = args
        self.kwargs = kwargs

    def funcArgs(self, *args, **kwargs) -> None:
        self.args = args
        self.kwargs = kwargs

    def run(self, returnVal: Any | Equation, Handling: bool = True, styling: bool = True) -> None | bool:
        if Handling:
            print(f"{self.name.title()}: {self.desc}", end=" - ", flush=True)

        funcVal: Any = self.func(*self.args, **self.kwargs)
        if isinstance(returnVal, Equation):
            passed: bool = returnVal.check(funcVal)

        else:
            passed: bool = funcVal == returnVal

        if Handling:
            if styling:
                con.print("[green bold]Passed" if passed else "[red bold]Failed")
                if not passed:
                    text = f"  Expected {returnVal} of type {type(returnVal).__name__} : Got {funcVal} of type {type(funcVal).__name__}  "
                    con.print(f"[red]/{"-"*len(text)}\\\n|{" "*len(text)}|\n|[bold]{text}[/bold]|\n|{" "*len(text)}|\n\\{"-"*len(text)}/")

            else:
                print("Passed" if passed else "Failed")
                if not passed:
                    text = f"  Expected {returnVal} of type {type(returnVal).__name__} : Got {funcVal} of type {type(funcVal).__name__}  "
                    print(f"/{"-"*len(text)}\\\n|{" "*len(text)}|\n|{text}|\n|{" "*len(text)}|\n\\{"-"*len(text)}/")

        return passed

class FeatureTest:

    def __init__(self, name: str, description: str, *tests) -> None:
        self.name: str = name
        self.description: str = description
        self.tests: list[Test] = list(tests)

    def addTest(self, test: Test) -> None:
        self.tests.append(test)

    def run(self, *args: tuple[list[Any] | dict[str, Any | list[Any]]], styling: bool = True) -> None:
        if styling:
            txt = f" Running [cyan]{self.name.title()}[/cyan]:"
            con.print(txt, end=" ")
            print(f"\033[38;5;8m{self.description}\033[0m\n{"-"*((len(txt) - 12) + len(self.description) + 1)}")

        state = [0, 0]
        failedNames: list[str] = []

        for params, test in zip(args, self.tests):
            if isinstance(params, list):
                if params == []:
                    test.run()
                    continue

                passed: bool = test.run(*params)
                state[0 if passed else 1] += 1
                if not passed:
                    failedNames.append(test.name)

            elif isinstance(params, dict):
                if params == {}:
                    test.run()
                    continue

                args = params["args"]
                params.pop("args")
                test.run(*args, **params)

        if styling:
            if state[0] == 0:
                print("\033[38;5;8m\033[1m0 Passed\033[0m\033[1m  ", end="")

            else:
                con.print(f"[green][bold]{state[0]} Passed[/green]  ", end="")

            if state[1] > 0:
                con.print(f"[red][bold]{state[1]} Failed[/bold]\nFailed Tests: [bold]{"[/bold], [bold]".join(failedNames)}")

            else:
                print("\033[38;5;8m\033[1m0 Failed")

if __name__ == "__main__":
    def add(a: int, b: int) -> int:
        import time
        time.sleep(3)
        return a + b

    tst = UnitTest("add", "adds 2 integer numbers", add)
    tst.funcArgs(2, 2)

    t = FeatureTest("Arithmatic", "Adding, Subtracting, Multiplying, and Dividing", tst, UnitTest("substract", "subtracts 2 ints", lambda a, b: a - b, 5, 3))
    t.addTest(UnitTest("multiply", "multiplies 2 ints", lambda a, b: a * b, 2, 4))
    t.addTest(UnitTest("divide", "divides 2 ints", lambda a, b: a / b, 8, 2))
    t.run([4], [2], [8], [4])