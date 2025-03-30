import os
from enum import Enum
from utils.date import get_yesterday


class FilepathConstant(Enum):
    """All file paths required for the system."""

    SETTINGS = os.path.realpath("./") + "/system.config.json"
    SNMP_DATA = os.path.realpath("./").split("/src")[0] + "/SNMP/data/" + get_yesterday()
    FILELOG = os.path.realpath("./").split("/src")[0] + "system.log"
