from fastapi import HTTPException
from fastapi import status as CodeStatus
from error import ErrorOperatorHandler

def ERROR_API(error: ErrorOperatorHandler):
    if error.get_code() == 404:
        return error_404(error.get_message())

def error_404(message: str):
    return HTTPException(
        status_code=CodeStatus.HTTP_404_NOT_FOUND, 
        detail=message
    )