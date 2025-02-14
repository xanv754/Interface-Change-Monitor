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

OPERATOR_NOT_FOUND = HTTPException(
    status_code=status.HTTP_404_NOT_FOUND,
    detail="Operator not found",
)

EQUIPMENT_NOT_FOUND = HTTPException(
    status_code=status.HTTP_404_NOT_FOUND,
    detail="Equipment not found",
)

INTERFACE_NOT_FOUND = HTTPException(
    status_code=status.HTTP_404_NOT_FOUND,
    detail="Interface not found",
)

ASSIGNMENT_NOT_FOUND = HTTPException(
    status_code=status.HTTP_404_NOT_FOUND,
    detail="Assignment not found",
)

ASSIGNMENTS_NOT_FOUND = HTTPException(
    status_code=status.HTTP_404_NOT_FOUND,
    detail="Assignments not found",
)