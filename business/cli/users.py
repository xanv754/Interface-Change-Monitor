import rich
from rich.prompt import Prompt
from business.libs.code import ResponseCode
from business.controllers.user import UserController
from business.models.user import UserModel
from constants.types import RoleTypes, UserStatusTypes
from utils.validate import Validate
from utils.config import Configuration
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
            role = Prompt.ask("Role", choices=[RoleTypes.ROOT, RoleTypes.ADMIN, RoleTypes.USER, RoleTypes.SOPORT], show_choices=True)
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

    
    def restore_password() -> None:
        """Restart password."""
        log.info("Restarting password...")
        configuration = Configuration()
        controller = UserController()
        try:
            username = Prompt.ask("Username")
            if not username: raise ValueError("Username cannot be empty")
            password = configuration.generate_default_password()
            response: ResponseCode = controller.update_password(username=username, password=password)
            if response.status == 200:
                log.info(f"Password restarted successfully to {username}")
                rich.print(f"[green]Password restarted successfully. Your new password is[/green] {password}")
                exit(0)
            else:
                raise Exception(response.message)
        except Exception as error:
            log.error(f"Restart password error. {error}")
            rich.print(f"[red]Error[/red] {error}")
            exit(1)