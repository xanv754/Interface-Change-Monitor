VERSION_ONE_PREFIX = "v1" # Current version of the API

LOGIN = f"{VERSION_ONE_PREFIX}" # Prefix for all routes of the login
OPERATOR = f"{VERSION_ONE_PREFIX}/operator" # Prefix for all routes of the operator
ADMINISTRATION = f"{VERSION_ONE_PREFIX}/administration" # Prefix for all routes of the administration
STATISTICS = f"{VERSION_ONE_PREFIX}/statistics" # Prefix for all routes of the statistics
HISTORY = f"{VERSION_ONE_PREFIX}/history" # Prefix for all routes of the history

OPERATOR_INFO = "info/me" # Prefix for all routes about the info of an operator logged in
OPERATOR_ASSIGMENT = f"{OPERATOR_INFO}/assignments" # Prefix for all routes about the assignments operator

ADMIN_OPERATOR_INFO = f"operator" # Prefix for all routes about the info operator
ADMIN_ASSIGNMENT_INFO = f"assignments" # Prefix for all routes about the info operator

STATISTICS_INFO = f"info" # Prefix for all routes about the statistics operator

HISTORY_INFO = f"info" # Prefix for all routes about the history operator