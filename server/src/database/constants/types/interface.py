from enum import Enum

class Date(Enum):
    TODAY = 'TODAY'
    YESTERDAY = 'YESTERDAY'
    OLD = 'OLD'

class Status(Enum):
    up = 'UP'
    down = 'DOWN'
    testing = 'TESTING'
    dormant = 'DORMANT'
    unknown = 'UNKNOWN'
    not_present = 'NOTPRESENT'
    lower_layer_down = 'LOWERLAYERDOWN'
    default = 'DEFAULT'