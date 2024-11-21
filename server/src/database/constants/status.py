from enum import Enum

class TypeStatus(Enum):
    """Valid for both the operational status (ifOperStatus) and the administrative status (ifAdminStatus)."""
    up = 'UP'
    down = 'DOWN'
    testing = 'TESTING'
    dormant = 'DORMANT'
    unknown = 'UNKNOWN'
    not_present = 'NOTPRESENT'
    lower_layer_down = 'LOWERLAYERDOWN'
    default = 'DEFAULT'