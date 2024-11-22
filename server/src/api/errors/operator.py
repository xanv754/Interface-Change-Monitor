from fastapi import HTTPException
from fastapi import status as CodeStatus

class ErrorAPIOperatorHandler:

    @staticmethod
    def ERROR_CODE(code: int, message: str):
        if code == 404: return ErrorAPIOperatorHandler.ERROR_CODE(message)

    def error_404(message: str):
        return HTTPException(
            status_code=CodeStatus.HTTP_404_NOT_FOUND, 
            detail=message
        )