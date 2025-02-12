import click
from datetime import datetime
from updater import reader

@click.command()
@click.option("--today", is_flag=True, help="Load all consults from today")
def main(today):
    if today:
        print(f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} —— Loading data from today...")
        reader()
        print(f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} —— Data loaded!")


if __name__ == "__main__":
    main()
