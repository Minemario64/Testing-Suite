from rich.console import Console

cli = Console(highlight=False)
for i in range(1, 100):
    try:
        cli.print("#", style=f'green{i}', end="")

    except:
        print("_", end="")