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

FAILED_UPDATE_OPERATOR = HTTPException(
    status_code=status.HTTP_400_BAD_REQUEST,
    detail="Failed to update operator",
)

FAILED_UPDATE_STATUS_ASSIGNMENT = HTTPException(
    status_code=status.HTTP_400_BAD_REQUEST,
    detail="Failed to update status assignment",
)

FAILED_DELETE_OPERATOR = HTTPException(
    status_code=status.HTTP_400_BAD_REQUEST,
    detail="Failed to delete operator",
)

FAILED_GET_STATISTICS = HTTPException(
    status_code=status.HTTP_400_BAD_REQUEST,
    detail="Failed get to statistics"
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

FAILED_TO_ASSIGN = HTTPException(
    status_code=status.HTTP_400_BAD_REQUEST,
    detail="Failed to assign",
)

FAILED_TO_REASSIGN = HTTPException(
    status_code=status.HTTP_400_BAD_REQUEST,
    detail="Failed to reassign",
)