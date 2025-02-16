"""
Prefixes of the endpoints of the API.

- VERSION_ONE_PREFIX: Current version of the API.
- LOGIN: Prefix for all routes of the login.
- OPERATOR: Prefix for all routes of the operator.
- ADMINISTRATION: Prefix for all routes of the administration.
- STATISTICS: Prefix for all routes of the statistics.
- HISTORY: Prefix for all routes of the history.
- OPERATOR_INFO: Prefix for all routes about the info of an operator logged in.
- OPERATOR_ASSIGMENT: Prefix for all routes about the assignments operator.
- ADMIN_OPERATOR_INFO: Prefix for all routes about the info operator.
- ADMIN_ASSIGNMENT_INFO: Prefix for all routes about the info operator.
- STATISTICS_INFO: Prefix for all routes about the statistics operator.
- HISTORY_INFO: Prefix for all routes about the history operator.
"""

VERSION_ONE_PREFIX = "v1"
LOGIN = f"{VERSION_ONE_PREFIX}"
OPERATOR = f"{VERSION_ONE_PREFIX}/operator"
ADMINISTRATION = f"{VERSION_ONE_PREFIX}/administration"
STATISTICS = f"{VERSION_ONE_PREFIX}/statistics"
HISTORY = f"{VERSION_ONE_PREFIX}/history"
OPERATOR_INFO = "info/me"
OPERATOR_ASSIGMENT = f"{OPERATOR_INFO}/assignments"
ADMIN_OPERATOR_INFO = f"operator"
ADMIN_ASSIGNMENT_INFO = f"assignments"
STATISTICS_INFO = f"info"
HISTORY_INFO = f"info"
