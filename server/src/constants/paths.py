import os
from enum import Enum
from utils import get_yesterday


class FilepathConstant(Enum):
    """All file paths required for the system."""

    SETTINGS = os.getcwd() + "/system.config.json"
    SNMP_DATA = os.getcwd().split("/src")[0] + "/SNMP/data/" + get_yesterday()
