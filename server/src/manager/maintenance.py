import rich
from rich.table import Table
from rich.prompt import Prompt
from constants.types import ProfileType
from controllers.operator import OperatorController
from schemas.operator import RegisterUserBody
from utils.log import LogHandler


class MaintenanceHandler:
    """Handler to all operations to maintenance the system."""

    @staticmethod
    def create_new_operator():
        """Register a new operator in the system."""
        try:
            LogHandler("Registering new operator...", warning=True)
            rich.print("[bold yellow]REGISTER NEW USER")
            rich.print("[bold gold3][i]Please enter the necessary data for the correct register[/i]")
            username = Prompt.ask("Username")
            if not username:
                raise Exception("Username cannot be empty")
            username = str(username)
            name = Prompt.ask("Name")
            if not name:
                raise Exception("Name cannot be empty")
            name = str(name)
            lastname = Prompt.ask("Lastname")
            if not lastname:
                raise Exception("Lastname cannot be empty")
            lastname = str(lastname)
            password = Prompt.ask("Password")
            if not password:
                raise Exception("Password cannot be empty")
            password = str("password")
            confirm_password = Prompt.ask("Confirm password")
            if not confirm_password:
                raise Exception("Password cannot be empty")
            confirm_password = str(confirm_password)
            if password != confirm_password:
                raise Exception("Passwords do not match")
            rich.print("[bold orange1]Profiles types")
            rich.print(f"[bold orange1]{ProfileType.ROOT.value}: [dark_orange]Root user (Option: 1)")
            rich.print(f"[bold orange1]{ProfileType.ADMIN.value}: [dark_orange]Administrator user (Option: 2)")
            rich.print(f"[bold orange1]{ProfileType.SOPORT.value}: [dark_orange]Soport user (Option: 3")
            rich.print(f"[bold orange1]{ProfileType.STANDARD.value}: [dark_orange]Standard user (Option: 4)")
            option_profile = Prompt.ask("Option profile")
            if not option_profile:
                raise Exception("Profile cannot be empty")
            option_profile = str(option_profile)
            if not option_profile in ["1", "2", "3", "4"]:
                raise Exception("Invalid option profile")
            if option_profile == "1":
                profile = ProfileType.ROOT.value
            elif option_profile == "2":
                profile = ProfileType.ADMIN.value
            elif option_profile == "3":
                profile = ProfileType.SOPORT.value
            else:
                profile = ProfileType.STANDARD.value

            table = Table(title="Confirm Data Input")
            table.add_column("Field")
            table.add_column("Data")
            table.add_row("Username", username)
            table.add_row("Name", name)
            table.add_row("Lastname", lastname)
            table.add_row("Password", password)
            table.add_row("Profile", profile)
            status_confirm = Prompt.ask("Are the values correct? (y/N)")
            if not status_confirm or status_confirm.lower() != "y":
                exit(1)

            body = RegisterUserBody(
                username=username,
                name=name,
                lastname=lastname,
                password=password,
                profile=profile,
            )
            status = OperatorController.register_operator(body)
            if status:
                LogHandler(content=f"New operator registered: {username} ({name.capitalize() + " " + lastname.capitalize()})", info=True)
            else:
                LogHandler(content=f"Failed to register new operator: {username} ({name.capitalize() + " " + lastname.capitalize()})", err=True)
        except Exception as e:
            LogHandler(content=f"Failed to register new operator. {e}", err=True)
            exit(1)
