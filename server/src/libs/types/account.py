from enum import Enum

class AccountType(Enum):
    """Type of status account for the operator entity."""
    active = 'ACTIVE'
    inactive = 'INACTIVE'
    deleted = 'DELETED'