from rich import print
from controllers import OperatorController
from schemas import RegisterUserBody
from utils import Log, is_valid_profile_type


def register_new_operator():
    """Register a new operator in the system."""
    try:
        print("[bold yellow]SYSTEM OF REGISTER NEW OPERATOR")
        print(
            "[bold gold3][i]Please enter the necessary data for the correct register[/i]"
        )
        print("[bright_green]Enter the username:")
        username = input()
        if not username:
            raise Exception("Username cannot be empty")
        print("[bright_green]Enter the name:")
        name = input()
        if not name:
            raise Exception("Name cannot be empty")
        print("[bright_green]Enter the lastname:")
        lastname = input()
        if not lastname:
            raise Exception("Lastname cannot be empty")
        print("[bright_green]Enter the password:")
        password = input()
        if not password:
            raise Exception("Password cannot be empty")
        print("[bright_green]Confirm the password:")
        password_confirm = input()
        if password != password_confirm:
            raise Exception("Passwords do not match")
        print("[bold orange1]Profiles types:")
        print("[bold orange1]ROOT: [dark_orange]Root user")
        print("[bold orange1]ADMIN: [dark_orange]Administrator")
        print("[bold orange1]STANDARD: [dark_orange]Standard user")
        print("[bold orange1]SOPORT: [dark_orange]Soport user")
        print("[bright_green]Enter the type profile:")
        profile = input()
        if not profile:
            raise Exception("Profile cannot be empty")
        profile = profile.upper()
        if not is_valid_profile_type(profile):
            raise Exception("Invalid profile")
        body = RegisterUserBody(
            username=username,
            name=name,
            lastname=lastname,
            password=password,
            profile=profile,
        )
        status = OperatorController.register_operator(body)
        if status:
            Log.save(
                f"New operator registered: {username} ({name.capitalize() + " " + lastname.capitalize()})",
                __file__,
                Log.info,
                console=True,
            )
        else:
            raise Exception("Operator not registered. More information in the log file")
    except KeyboardInterrupt:
        print("[bold red]Register interrupted. Exiting...")
    except Exception as e:
        Log.save(
            f"Error registering new operator. {e}", __file__, Log.error, console=True
        )
