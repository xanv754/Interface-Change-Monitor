from fastapi import HTTPException, status


class ResponseCode:
    """Class to manage response code."""
    status: int
    error: HTTPException | None = None

    def __init__(self, status: int, message: str | None = None):
        self.status = status
        if status == 400:
            self.error = self.__bad_request(message)
        elif status == 404:
            self.error = self.__not_found(message)
        elif status == 500:
            self.error = self.__server_error(message)

    def __bad_request(self, message: str) -> HTTPException:
        return HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=message,
        )
    
    def __not_found(self, message: str) -> HTTPException:
        return HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=message,
        )

    def __server_error(self, message: str | None = None) -> HTTPException:
        if message: detail=f"An error inexpected has occurred on the server. {message}",
        else: detail="An error inexpected has occurred on the server",
        return HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=detail,
        )
