from constants import InterfaceType, StatusType, StatusAssignmentType, AccountType, ProfileType

def is_valid_interface_type(value: str) -> bool:
    return value in InterfaceType._value2member_map_

def is_valid_status_type(value: str) -> bool:
    return value in StatusType._value2member_map_

def is_valid_status_assignment_type(value: str) -> bool:
    return value in StatusAssignmentType._value2member_map_

def is_valid_account_type(value: str) -> bool:
    return value in AccountType._value2member_map_

def is_valid_profile_type(value: str) -> bool:
    return value in ProfileType._value2member_map_