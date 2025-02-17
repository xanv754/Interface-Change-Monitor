import click
from datetime import datetime
from rich import print
from system import register_new_operator
from core import SystemConfig

@click.command()
@click.option("--register", is_flag=True, help="Register new operator")
@click.option("--configuration", is_flag=True, help="Export an new configuration file of the system")
@click.option("--reset", is_flag=True, help="Reset the configuration of the system")
def main(register, configuration, reset):
    if register:
        register_new_operator()
    elif configuration:    
        SystemConfig()
        print(
            f"[bold orange3]{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} [default] The configuration of the system has been [green1]created[default]!"
        )
    elif reset:
        status = SystemConfig().reset_config()
        if status:
            print(
                f"[bold orange3]{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} [default] The configuration of the system has been [green1]reset[default]!"
            )
        else:
            print(
                f"[bold orange3]{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} [default] The configuration of the system has not been [red3]reset[default]!"
            )

        


if __name__ == "__main__":
    main()
