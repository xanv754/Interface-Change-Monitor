import click
from system import register_new_operator


@click.command()
@click.option("--register", is_flag=True, help="Register new operator")
def main(register):
    if register:
        register_new_operator()


if __name__ == "__main__":
    main()
