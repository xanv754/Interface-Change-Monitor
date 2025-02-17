import click
from system import register_new_operator
from core import SystemConfig

@click.command()
@click.option("--register", is_flag=True, help="Register new operator")
@click.option("--configuration", is_flag=True, help="Export an new configuration file of the system")
def main(register, configuration):
    if register:
        register_new_operator()
    elif configuration:    
        SystemConfig()


if __name__ == "__main__":
    main()
