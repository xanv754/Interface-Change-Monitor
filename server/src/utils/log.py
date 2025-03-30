from rich.console import Console, Group
from rich.text import Text
from rich.panel import Panel
from typing import List
from datetime import datetime
from constants.paths import FilepathConstant


class LogHandler:
    """Handler to save and print all log messages."""

    __stdout: List[Text] = []
    __console: Console

    def __new__(cls, *args, **kwargs):
        if not cls.__instance:
            cls.__instance = super().__new__(cls)
        return cls.__instance

    def __init__(self, content: str, path: str = "unknown", err: bool = False, warning: bool = False, info: bool = False, cprint: bool = True) -> None:
        if not hasattr(self, "__initialized"):
            self.__console = Console()
        if cprint:
            self.console_print(message=content, path=path, err=err, warning=warning, info=info)
        if path != "unknown":
            path = path.split("/")[-2]
        if err:
            log = f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} Error ({path}) {content} \n"
        elif warning:
            log = f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} Warning ({path}) {content} \n"
        else:
            log = f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} Info ({path}) {content} \n"
        with open(FilepathConstant.FILELOG.value, "a") as file:
            file.write(log)
            file.close()

    def console_print(self, message: str, path: str = "unknown", err: bool = False, warning: bool = False, info: bool = False) -> None:
        """Print a message in the console.

        Parameters
        ----------
        message : str
            Content of the message.
        path : str
            Path of file that execute log.
        err : bool
            If True, this log is an error message.
        warning : bool
            If True, this log is a warning message.
        info : bool
            If True, this log is a info message.
        """
        if path != "unknown":
            path = path.split("/")[-2]
            if err:
                content = Text.assemble(
                    (f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}", "orange3"),
                    (" Error", "red3"),
                    (f" ({path})", "deep_sky_blue3"),
                    (f" {message}", "default")
                )
            elif warning:
                content = Text.assemble(
                    (f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}", "orange3"),
                    (" Warning", "bright_yellow"),
                    (f" ({path})", "deep_sky_blue3"),
                    (f" {message}", "default")
                )
            elif info:
                content = Text.assemble(
                    (f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}", "orange3"),
                    (" Info", "green3"),
                    (f" ({path})", "deep_sky_blue3"),
                    (f" {message}", "default")
                )
            else:
                content = Text.assemble(
                    (f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}", "orange3"),
                    (" Info", "default"),
                    (f" ({path})", "deep_sky_blue3"),
                    (f" {message}", "default")
                )
        else:
            if err:
                content = Text.assemble(
                    (f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}", "orange3"),
                    (" Error", "red3"),
                    (f" {message}", "default")
                )
            elif warning:
                content = Text.assemble(
                    (f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}", "orange3"),
                    (" Warning", "bright_yellow"),
                    (f" {message}", "default")
                )
            elif info:
                content = Text.assemble(
                    (f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}", "orange3"),
                    (" Info", "green3"),
                    (f" {message}", "default")
                )
            else:
                content = Text.assemble(
                    (f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}", "orange3"),
                    (" Info", "default"),
                    (f" {message}", "default")
                )
        self.__stdout.append(content)
        group = Group(*self.__stdout)
        panel = Panel(group, title="ICM", style="dark_blue")
        self.__console.clear()
        self.__console.print(panel)
