import logging
from pathlib import Path
from logging.handlers import TimedRotatingFileHandler


LOGS = "/var/log/icm"
LOG_FORMAT = "%(asctime)s %(levelname)s %(message)s"
DATE_FORMAT = "%Y-%m-%d %H:%M:%S"
FORMATTER = logging.Formatter(LOG_FORMAT, DATE_FORMAT)


class LogHandler:
    """Handler to realize all operation about log system."""
    __file_handler: TimedRotatingFileHandler
    logger: logging.Logger

    def __init__(self) -> None:
        try:
            folder_exist = self.create_file()
            if not folder_exist: return
            self.__file_handler = TimedRotatingFileHandler(
                f"{LOGS}/icm.log",
                when="W0",
                interval=1,
                backupCount=4,
                encoding="utf-8",
                utc=True
            )
            self.__file_handler.setFormatter(FORMATTER)
            logging.basicConfig(level=logging.INFO, handlers=[self.__file_handler])
            self.logger = logging.getLogger(__name__)
        except Exception as error:
            print(f"[bold red3]Failed to create log file. {error}")

    def create_file(self) -> bool:
        """Create file to save logs."""
        try:
            path = Path(LOGS)
            path.mkdir(parents=True, exist_ok=True)
            return True
        except Exception as error:
            print(f"[bold red3]Failed to create log folder. {error}")
            return False


logHandler = LogHandler()
log = logHandler.logger