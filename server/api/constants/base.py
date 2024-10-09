import os

class BaseConstants:
    FILEPATH = ""
    MONTHS_TO_KEEP = 2

    def __init__(self) -> None:
        current_filepath = os.path.dirname(__file__)
        filepath_dir = os.path.join(current_filepath, "../data")
        self.FILEPATH = filepath_dir

constants = BaseConstants()