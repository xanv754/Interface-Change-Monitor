class ErrorHandler:
    __code: int
    __message: str

    def get_code(self) -> int:
        return self.__code    

    def set_code(self, code: int):
        self.__code = code

    def get_message(self) -> str:
        return self.__message

    def set_message(self, message: str):
        self.__message = message