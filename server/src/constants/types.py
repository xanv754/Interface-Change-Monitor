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
