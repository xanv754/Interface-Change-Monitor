from error.interface import code as CODE
from error.interface import message as MESSAGE
from error.error import ErrorHandler

class ErrorInterfaceHandler(ErrorHandler):
    def __init__(self, code: str):
        if code == CODE.ERROR_400_BAD_REQUEST:
            self.set_code(400)
            self.set_message(MESSAGE.ERROR_400_BAD_REQUEST)
        elif code == CODE.ERROR_400_ID_REQUIRED:
            self.set_code(400)
            self.set_message(MESSAGE.ERROR_400_ID_REQUIRED)
        elif code == CODE.ERROR_400_IP_REQUIRED:
            self.set_code(400)
            self.set_message(MESSAGE.ERROR_400_IP_REQUIRED)
        elif code == CODE.ERROR_400_COMMUNITY_REQUIRED:
            self.set_code(400)
            self.set_message(MESSAGE.ERROR_400_COMMUNITY_REQUIRED)
        elif code == CODE.ERROR_400_INDEX_REQUIRED:
            self.set_code(400)
            self.set_message(MESSAGE.ERROR_400_INDEX_REQUIRED)
        elif code == CODE.ERROR_400_SYSNAME_REQUIRED:
            self.set_code(400)
            self.set_message(MESSAGE.ERROR_400_SYSNAME_REQUIRED)
        elif code == CODE.ERROR_400_DATE_REQUIRED:
            self.set_code(400)
            self.set_message(MESSAGE.ERROR_400_DATE_REQUIRED)
        elif code == CODE.ERROR_404_EQUIPMENT_NOT_FOUND:
            self.set_code(404)
            self.set_message(MESSAGE.ERROR_404_EQUIPMENT_NOT_FOUND)
        elif code == CODE.ERROR_404_INTERFACE_NOT_FOUND:
            self.set_code(404)
            self.set_message(MESSAGE.ERROR_404_INTERFACE_NOT_FOUND)
        elif code == CODE.ERROR_500_UNKNOWN:
            self.set_code(500)
            self.set_message(MESSAGE.ERROR_500_UNKNOWN)