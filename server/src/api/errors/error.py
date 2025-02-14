from fastapi import HTTPException, status

# NOTE: ERRORS OF LOGIN
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


# NOTE: ERRORS UNKNOWN
INTERNAL_SERVER_ERROR = HTTPException(
    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
    detail="An unpexpected error has occurred",
)


# NOTE: ERRORS OF EQUIPMENT
EQUIPMENT_NOT_FOUND = HTTPException(
    status_code=status.HTTP_404_NOT_FOUND,
    detail="Equipment not found",
)


# NOTE: ERRORS OF INTERFACE
INTERFACE_NOT_FOUND = HTTPException(
    status_code=status.HTTP_404_NOT_FOUND,
    detail="Interface not found",
)


# NOTE: ERRORS OF OPERATOR
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


# NOTE: ERRORS OF ASSIGNMENT
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


# NOTE: ERRORS OF STATISTICS
STATISTICS = HTTPException(
    status_code=status.HTTP_400_BAD_REQUEST,
    detail="Failed get to statistics"
)


