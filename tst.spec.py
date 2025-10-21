from tst import Hi
import tester

tester.GLOBALS |= globals()
tester.describe("Says Hi", '''
it("Says Hi to people", """
    passed(Hi("bob") == "Hello, Bob!")
""")
''')