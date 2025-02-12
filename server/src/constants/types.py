from enum import Enum


class AccountType(Enum):
    ACTIVE = "ACTIVE"
    INACTIVE = "INACTIVE"
    DELETED = "DELETED"


class ProfileType(Enum):
    ROOT = "ROOT"
    ADMIN = "ADMIN"
    STANDARD = "STANDARD"
    SOPORT = "SOPORT"


class StatusAssignmentType(Enum):
    PENDING = "PENDING"
    INSPECTED = "INSPECTED"
    REDISCOVERED = "REDISCOVERED"


class StatusType(Enum):
    UP = "UP"
    DOWN = "DOWN"
    TESTING = "TESTING"
    DORMANT = "DORMANT"
    UNKNOWN = "UNKNOWN"
    NOTPRESENT = "NOTPRESENT"
    LOWERLAYERDOWN = "LOWERLAYERDOWN"
    DEFAULT = "DEFAULT"


class InterfaceType(Enum):
    NEW = "NEW"
    OLD = "OLD"