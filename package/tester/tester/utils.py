import os

def countUntilLand(ln: str) -> int:
    for i, char in enumerate(ln, 0):
        if char != " ":
            return i
    raise ValueError("Text '{ln}' has no land (non-whitespace)")

def traverseFuncStr(text: str, start: int = 0) -> str:
    funcLevel: int = 0
    result: str = ""
    for char in text[start::]:
        match char:
            case "(":
                if funcLevel > 0:
                    result += char

                funcLevel += 1

            case ")":
                if funcLevel == 0:
                    return '""'

                funcLevel -= 1
                if funcLevel > 0:
                    result += char

                if funcLevel == 0:
                    return result

            case _:
                if funcLevel > 0:
                    result += char

    return '""'

def clear() -> None:
    os.system("powershell clear")

if __name__ == "__main__":
    import re
    text = '''
it("Adds 2 numbers", """
    time.sleep(1.2)
    result = add(2, 2)
    passed(result == 4)
""")
it("Multiplies 2 numbers", """
    time.sleep(0.5)
    result = multiply(4, 8)
    passed(result == 32)
""")
'''
    passedPattern = re.compile(r" *it\(")
    ln = text.split("\n")[1]
    lns = text.split("\n")
    i = 1
    if matched := passedPattern.match(ln):
        print((len("\n".join(lns[0:i-1])) - 1))
        print(matched.pos + (len("\n".join(lns[0:i-1]))))
        text = f"{" "*countUntilLand(ln)}testResults.append(it({traverseFuncStr(text, matched.pos + (len("\n".join(lns[0:i-1]))))}))"
        print(text)