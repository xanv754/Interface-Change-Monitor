"""Names of the tables of the database."""

from enum import Enum


class Tables(Enum):
    """Names of the tables of the database.

    - EQUIPMENT: Table of the equipment.
    - INTERFACE: Table of the interface.
    - OPERATOR: Table of the operator.
    - ASSIGNMENT: Table of the assignment.
    """

    EQUIPMENT = "equipment"
    INTERFACE = "interface"
    OPERATOR = "operator"
    ASSIGNMENT = "assignment"
