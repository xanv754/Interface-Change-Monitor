from enum import Enum

class ProfileType(Enum):
    """Type of profile account for the operator entity."""
    root = 'SUPERADMIN'
    admin = 'ADMIN'
    user = 'STANDARD'
    soport = 'SOPORT'