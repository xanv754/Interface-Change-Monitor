"""
ALl errors HTTP of the API.

- UNATHORIZED_USER: Error when the user is not authorized.
- INVALID_TOKEN: Error when the token is invalid.
- INTERNAL_SERVER_ERROR: Error when an unpexpected error has occurred.
- EQUIPMENT_NOT_FOUND: Error when the equipment is not found.
- INTERFACE_NOT_FOUND: Error when the interface is not found.
- OPERATOR_NOT_FOUND: Error when the operator is not found.
- UPDATE_OPERATOR: Error when the operator is not updated.
- DELETE_OPERATOR: Error when the operator is not deleted.
- ASSIGNMENT_NOT_FOUND: Error when the assignment is not found.
- UPDATE_STATUS_ASSIGNMENT: Error when the status assignment is not updated.
- ASSIGN: Error when the assignment is not assigned.
- REASSIGN: Error when the assignment is not reassigned.
- STATISTICS: Error when the statistics are not obtained.
"""

from fastapi import HTTPException, status


UNATHORIZED_USER = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Unauthorized user",
    headers={"WWW-Authenticate": "Bearer"},
)
INVALID_TOKEN = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Invalid token",
    headers={"WWW-Authenticate": "Bearer"},
)
INTERNAL_SERVER_ERROR = HTTPException(
    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
    detail="An unpexpected error has occurred",
)
EQUIPMENT_NOT_FOUND = HTTPException(
    status_code=status.HTTP_404_NOT_FOUND,
    detail="Equipment not found",
)
INTERFACE_NOT_FOUND = HTTPException(
    status_code=status.HTTP_404_NOT_FOUND,
    detail="Interface not found",
)
OPERATOR_NOT_FOUND = HTTPException(
    status_code=status.HTTP_404_NOT_FOUND,
    detail="Operator not found",
)
UPDATE_OPERATOR = HTTPException(
    status_code=status.HTTP_400_BAD_REQUEST,
    detail="Failed to update operator",
)
DELETE_OPERATOR = HTTPException(
    status_code=status.HTTP_400_BAD_REQUEST,
    detail="Failed to delete operator",
)
ASSIGNMENT_NOT_FOUND = HTTPException(
    status_code=status.HTTP_404_NOT_FOUND,
    detail="Assignment not found",
)
UPDATE_STATUS_ASSIGNMENT = HTTPException(
    status_code=status.HTTP_400_BAD_REQUEST,
    detail="Failed to update status assignment",
)
ASSIGN = HTTPException(
    status_code=status.HTTP_400_BAD_REQUEST,
    detail="Failed to assign",
)
REASSIGN = HTTPException(
    status_code=status.HTTP_400_BAD_REQUEST,
    detail="Failed to reassign",
)
STATISTICS = HTTPException(
    status_code=status.HTTP_400_BAD_REQUEST, detail="Failed get to statistics"
)
