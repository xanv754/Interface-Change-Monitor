class ErrorCodeOperator:
    @property
    def ERROR_00_UNKNOWN(self) -> int:
        return 0

    @property
    def ERROR_10_OPERATOR_NOT_FOUND(self) -> int:
        return 10
    
    @property
    def ERROR_11_BAD_CREATE(self) -> int:
        return 11

    @property
    def ERROR_20_USERNAME_REQUIRED(self) -> int:
        return 20
    
    @property
    def ERROR_21_ALREADY_EXISTS(self) -> int:
        return 21