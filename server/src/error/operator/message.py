class ErrorMessageOperator:
    @property
    def ERROR_00_UNKNOWN(self) -> str:
        return "An unknown error has occurred."

    @property
    def ERROR_10_OPERATOR_NOT_FOUND(self) -> str:
        return "The operators or operator was not found."
    
    @property
    def ERROR_11_BAD_CREATE(self) -> str:
        return "The request sent does not contain the required fields or parameters."

    @property
    def ERROR_20_USERNAME_REQUIRED(self) -> str:
        return "The username's operator is required."
    
    @property
    def ERROR_21_ALREADY_EXISTS(self) -> str:
        return "The username's operator isn't valid."