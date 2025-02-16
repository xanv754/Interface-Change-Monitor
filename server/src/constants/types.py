"""
All types necessary for the system.

- **AccountType:** Type of status of account of the operator.
- **ProfileType:** Type of profile of the operator.
- **StatusAssignmentType:** Type of status of the assignment.
- **StatusType:** Type of status of the interface to SNMP consult.
- **InterfaceType:** Type of interface.
"""

from enum import Enum


class AccountType(Enum):
    """Type of account of the operator.

    - ACTIVE: Type of active account. You can use the system.
    - INACTIVE: Type of inactive account. You cannot use the system.
    - DELETED: Account type will soon be deleted. You cannot use the system.
    """

    ACTIVE = "ACTIVE"
    INACTIVE = "INACTIVE"
    DELETED = "DELETED"


class ProfileType(Enum):
    """Type of profile of the operator.

    - ROOT: Type of root profile. Has full privileges in the system.
    - ADMIN: Type of admin profile. You have permissions to assign and view all statistics in the system.
    - STANDARD: Type of standard profile. Basic user, who can only receive assignments and view his own statistics.
    - SOPORT: Type of support profile. Has full privileges in the system plus some for system maintenance.
    """

    ROOT = "ROOT"
    ADMIN = "ADMIN"
    STANDARD = "STANDARD"
    SOPORT = "SOPORT"


class StatusAssignmentType(Enum):
    """Type of status of an assignment.

    - PENDING: Type of pending assignment. The assignment has not been reviewed
    - INSPECTED: Type of inspected assignment. The assignment has been reviewed, but does not require rediscovery.
    - REDISCOVERED: Type of rediscovered assignment. The assignment has been reviewed, and requires rediscovery.
    """

    PENDING = "PENDING"
    INSPECTED = "INSPECTED"
    REDISCOVERED = "REDISCOVERED"


class StatusType(Enum):
    """Type of status of the interface in an SNMP consult."""

    UP = "UP"
    DOWN = "DOWN"
    TESTING = "TESTING"
    DORMANT = "DORMANT"
    UNKNOWN = "UNKNOWN"
    NOTPRESENT = "NOTPRESENT"
    LOWERLAYERDOWN = "LOWERLAYERDOWN"
    DEFAULT = "DEFAULT"


class InterfaceType(Enum):
    """Type of an interface.

    - NEW: Interface with the data of the last SNMP consult.
    - OLD: Interface with the data of the previous SNMP consult.
    """

    NEW = "NEW"
    OLD = "OLD"
