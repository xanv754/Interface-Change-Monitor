from enum import Enum

class Profile(Enum):
    super_admin = 'SUPERADMIN'
    admin = 'ADMIN'
    standard = 'STANDARD'
    soport = 'SOPORT'

class StatusAccount(Enum):
    active = 'ACTIVE'
    inactive = 'INACTIVE'