from os import getcwd
from datetime import datetime
from rich import print
from constants import LogType

FILELOG = getcwd().split("src")[0] + "system.log"


class Log:
    """Class to log messages."""

    error: LogType = LogType.ERROR
    warning: LogType = LogType.WARNING
    info: LogType = LogType.INFO

    @staticmethod
    def save(
        content: str,
        modulo: str = "unknown",
        type: LogType = LogType.INFO,
        console: bool = False,
    ) -> None:
        """Save a message in the log file.

        Parameters
        ----------
        content : str
            Content of the message.
        modulo : str
            Module of the message.
        type : LogType
            Type of the message.
        console : bool
            If True, the message will be printed in the console.
        """
        if console:
            Log.impr(content, modulo, type)
        if modulo != "unknown":
            modulo = modulo.split("/")[-1]
        with open(FILELOG, "a") as file:
            file.write(
                f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} {type.value} [{modulo}] {content} \n"
            )
            file.close()

    @staticmethod
    def impr(
        content: str, modulo: str = "unknown", type: LogType = LogType.INFO
    ) -> None:
        """Print a message in the console.

        Parameters
        ----------
        content : str
            Content of the message.
        modulo : str
            Module of the message.
        type : LogType
            Type of the message.
        """
        if modulo != "unknown":
            modulo = modulo.split("/")[-1]
        if type == LogType.ERROR:
            print(
                f"[bold orange3]{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} [bold red]{type.value} [bold blue]({modulo}) [default]{content}"
            )
        elif type == LogType.WARNING:
            print(
                f"[bold orange3]{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} [bold bright_yellow]{type.value} [bold blue]({modulo}) [default]{content}"
            )
        else:
            print(
                f"[bold orange3]{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} [bold green4]{type.value} [bold blue]({modulo}) [default]{content}"
            )
