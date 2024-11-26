from fastapi import HTTPException
from fastapi import status as CodeStatus
from error import ErrorOperatorHandler

def ERROR_API(error: ErrorOperatorHandler) -> BaseException:
    if error.get_code() == 400:
        return error_400(error.get_message())
    if error.get_code() == 403:
        return error_403(error.get_message())
    if error.get_code() == 404:
        return error_404(error.get_message())
    if error.get_code() == 500:
        return error_500(error.get_message())
    
def error_400(message: str):
    return HTTPException(
        status_code=CodeStatus.HTTP_400_BAD_REQUEST, 
        detail=message
    )

def error_403(message: str):
    return HTTPException(
        status_code=CodeStatus.HTTP_403_FORBIDDEN, 
        detail=message
    )

def error_404(message: str):
    return HTTPException(
        status_code=CodeStatus.HTTP_404_NOT_FOUND, 
        detail=message
    )

def error_500(message: str):
    return HTTPException(
        status_code=CodeStatus.HTTP_500_INTERNAL_SERVER_ERROR, 
        detail=message
    )