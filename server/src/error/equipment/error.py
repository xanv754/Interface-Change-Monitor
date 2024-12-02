from error.error import ErrorHandler
from error.equipment import code as CODE
from error.equipment import message as MESSAGE

class ErrorEquipmentHandler(ErrorHandler):
    def __init__(self, code: str):
        if code == CODE.ERROR_400_ID_REQUIRED:
            self.set_code(400)
            self.set_message(MESSAGE.ERROR_400_ID_REQUIRED)
        elif code == CODE.ERROR_400_IP_REQUIRED:
            self.set_code(400)
            self.set_message(MESSAGE.ERROR_400_IP_REQUIRED)
        elif code == CODE.ERROR_400_COMMUNITY_REQUIRED:
            self.set_code(400)
            self.set_message(MESSAGE.ERROR_400_COMMUNITY_REQUIRED)
        elif code == CODE.ERROR_400_SYSNAME_REQUIRED:
            self.set_code(400)
            self.set_message(MESSAGE.ERROR_400_SYSNAME_REQUIRED)
        elif code == CODE.ERROR_404_EQUIPMENT_NOT_FOUND:
            self.set_code(404)
            self.set_message(MESSAGE.ERROR_404_EQUIPMENT_NOT_FOUND)
        elif code == CODE.ERROR_409_EQUIPMENT_ALREADY_EXISTS:
            self.set_code(409)
            self.set_message(MESSAGE.ERROR_409_EQUIPMENT_ALREADY_EXISTS)
        elif code == CODE.ERROR_500_UNKNOWN:
            self.set_code(500)
            self.set_message(MESSAGE.ERROR_500_UNKNOWN)