class ErrorHandler:
    __code: int

    def get_code(self) -> int:
        return self.__code    

    def set_code(self, code: int):
        self.__code = code