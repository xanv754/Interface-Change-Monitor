from api.errors.api import (
    UNATHORIZED_USER,
    INVALID_TOKEN,
    INTERNAL_SERVER_ERROR,
    OPERATOR_NOT_FOUND,
    EQUIPMENT_NOT_FOUND,
    INTERFACE_NOT_FOUND,
    ASSIGNMENT_NOT_FOUND,
    ASSIGNMENTS_NOT_FOUND
)
from api.routes.login import router as LoginRouter
from api.routes.login import login
from api.routes.operator import router as OperatorRouter
from api.constants.prefix import (
    VERSION_ONE_PREFIX,
    OPERATOR_PREFIX,
    LOGIN_PREFIX,
)