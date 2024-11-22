from error.error import ErrorHandler
from error.operator.message import ErrorMessageOperator

class ErrorOperatorHandler(ErrorHandler):
    __message: str

    def __init__(self, code: int):
        self.set_code(code)
        # if code == 10: self.__message = ErrorMessageOperator.ERROR_10_OPERATOR_NOT_FOUND
        if code == 10: self.__message = "asdkajsdlkdjs"

    @property
    def code(self) -> int:
        return self.get_code()
    
    @property
    def message(self) -> str:
        return self.__message