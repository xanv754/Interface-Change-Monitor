from enum import Enum


class AssignmentSchemaDB(Enum):
    """Names of the columns of the assignment table."""

    ID = "id"
    CHANGE_INTERFACE = "changeinterface"
    OLD_INTERFACE = "oldinterface"
    OPERATOR = "operator"
    DATE_ASSIGNMENT = "dateassignment"
    STATUS_ASSIGNMENT = "statusassignment"
    ASSIGNED_BY = "assignedby"
    UPDATED_AT = "updatedat"
