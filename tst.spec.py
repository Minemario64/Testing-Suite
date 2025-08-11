from tst import Hi
import __init__ as tester

tester.GLOBALS |= globals()
tester.describe("Says Hi", '''
it("Says Hi to people", """
    passed(Hi("bob") == "Hello, Bob!")
""")
''')