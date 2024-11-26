from error.error import ErrorHandler
from error.assignment import message as MESSAGE
from error.assignment import code as CODE

class ErrorAssignmentHandler(ErrorHandler):
    def __init__(self, code: str):
        if code == CODE.ERROR_400_USERNAME_REQUIRED:
            self.set_code(400)
            self.set_message(MESSAGE.ERROR_400_USERNAME_REQUIRED)
        if code == CODE.ERROR_400_ID_INTERFACE_REQUIRED:
            self.set_code(400)
            self.set_message(MESSAGE.ERROR_400_ID_INTERFACE_REQUIRED)
        if code == CODE.ERROR_400_DATE_REQUIRED:
            self.set_code(400)
            self.set_message(MESSAGE.ERROR_400_DATE_REQUIRED)
        if code == CODE.ERROR_400_STATUS_REQUIRED:
            self.set_code(400)
            self.set_message(MESSAGE.ERROR_400_STATUS_REQUIRED)
        if code == CODE.ERROR_400_NAME_REQUIRED:
            self.set_code(400)
            self.set_message(MESSAGE.ERROR_400_NAME_REQUIRED)
        if code == CODE.ERROR_400_STATUS_NO_VALID:
            self.set_code(400)
            self.set_message(MESSAGE.ERROR_400_STATUS_NO_VALID)
        if code == CODE.ERROR_404_OPERATOR_NOT_FOUND:
            self.set_code(404)
            self.set_message(MESSAGE.ERROR_404_OPERATOR_NOT_FOUND)
        if code == CODE.ERROR_404_ASSIGNMENT_NOT_FOUND:
            self.set_code(404)
            self.set_message(MESSAGE.ERROR_404_ASSIGNMENT_NOT_FOUND)
        if code == CODE.ERROR_500_UNKNOWN:
            self.set_code(500)
            self.set_message(MESSAGE.ERROR_500_UNKNOWN)