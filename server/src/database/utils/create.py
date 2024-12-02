from error import ErrorHandler

def log(error: ErrorHandler | None = None, error_console: str | None = None) -> None:
    # TODO: Write the message in the log
    if error_console: print("Error:", error_console)
    pass