from error.error import ErrorHandler
from error.operator import message as MESSAGE
from error.operator import code as CODE

class ErrorOperatorHandler(ErrorHandler):
    def __init__(self, code: str):
        if code == CODE.ERROR_400_BAD_CREATE:
            self.set_code(400)
            self.set_message(MESSAGE.ERROR_400_BAD_CREATE)
        if code == CODE.ERROR_400_USERNAME_REQUIRED:
            self.set_code(400)
            self.set_message(MESSAGE.ERROR_400_USERNAME_REQUIRED)
        if code == CODE.ERROR_400_OPTION_REQUIRED:
            self.set_code(400)
            self.set_message(MESSAGE.ERROR_400_OPTION_REQUIRED)
        if code == CODE.ERROR_400_PROFILE_NOT_VALID:
            self.set_code(400)
            self.set_message(MESSAGE.ERROR_400_PROFILE_NOT_VALID)
        if code == CODE.ERROR_400_STATUS_NOT_VALID:
            self.set_code(400)
            self.set_message(MESSAGE.ERROR_400_STATUS_NOT_VALID)
        if code == CODE.ERROR_400_DELETE_NOT_VALID:
            self.set_code(400)
            self.set_message(MESSAGE.ERROR_400_DELETE_NOT_VALID)
        if code == CODE.ERROR_400_ALREADY_EXISTS:
            self.set_code(400)
            self.set_message(MESSAGE.ERROR_400_ALREADY_EXISTS)
        if code == CODE.ERROR_403_PROFILE_NOT_ALLOWED:
            self.set_code(403)
            self.set_message(MESSAGE.ERROR_403_PROFILE_NOT_ALLOWED)
        if code == CODE.ERROR_404_OPERATOR_NOT_FOUND:
            self.set_code(400)
            self.set_message(MESSAGE.ERROR_404_OPERATOR_NOT_FOUND)
        if code == CODE.ERROR_500_UNKNOWN:
            self.set_code(500)
            self.set_message(MESSAGE.ERROR_500_UNKNOWN)