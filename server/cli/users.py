import rich
from rich.prompt import Prompt
from constants.code import ResponseCode
from constants.types import RoleTypes, UserStatusTypes
from controllers.user import UserController
from models.user import UserModel
from utils.validate import Validate
from utils.log import log


class UserCLI:
    
    @staticmethod
    def register() -> None:
        """Register a new user."""
        log.info("Registering a new user...")
        controller = UserController()
        try:
            username = Prompt.ask("Username")
            if not username: raise ValueError("Username cannot be empty")
            password = Prompt.ask("Password")
            if not password: raise ValueError("Password cannot be empty")
            name = Prompt.ask("Name")
            if not name: raise ValueError("Name cannot be empty")
            lastname = Prompt.ask("Lastname")
            if not lastname: raise ValueError("Lastname cannot be empty")
            role = Prompt.ask("Role", choices=[RoleTypes.ROOT, RoleTypes.ADMIN, RoleTypes.USER], show_choices=True)
            if not role: raise ValueError("Role cannot be empty")
            if not Validate.role(role): raise ValueError("Role not valid")
            status = UserStatusTypes.ACTIVE
            new_user = UserModel(
                username=username, password=password,
                name=name, lastname=lastname,
                role=role, status=status,
                created_at=None, updated_at=None
            )
            confirm = Prompt.ask("Confirm registration?", choices=["y", "n"], show_choices=True, default="y")
            if confirm.lower() != "y": 
                log.info("Registration canceled")
                rich.print(f"[gold3]Registration canceled")
                exit(0)
            response: ResponseCode = controller.new_user(new_user=new_user)
            if response.status == 201:
                log.info("User registered successfully")
                rich.print(f"[green]User registered successfully[/green]")
                exit(0)
            else:
                raise Exception(response.message)
        except Exception as error:
            log.error(f"Register error. {error}")
            rich.print(f"[red]Error[/red] {error}")
            exit(1)