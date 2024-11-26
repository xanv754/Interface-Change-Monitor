from error.error import ErrorHandler
from error.operator import message as MESSAGE
from error.operator import code as CODE

class ErrorOperatorHandler(ErrorHandler):
    def __init__(self, code: int):
        self.set_code(code)
        if code == CODE.ERROR_404_OPERATOR_NOT_FOUND:
            self.set_message(MESSAGE.ERROR_404_OPERATOR_NOT_FOUND)