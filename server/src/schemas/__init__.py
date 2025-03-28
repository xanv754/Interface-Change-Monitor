from schemas.token import TokenDataSchema, TokenResponseSchema
from schemas.operator import (
    OperatorSchema,
    UserSchema,
    UpdatePasswordBody,
    UpdateProfileBody,
    UpdateAccountBody,
    RegisterUserBody,
    UpdateUserRootBody,
    UpdateUserStandardBody
)
from schemas.equipment import (
    EquipmentSchema,
    RegisterEquipmentBody
)
from schemas.interface import (
    InterfaceSchema,
    RegisterInterfaceBody
)
from schemas.assignment import (
    AssignmentSchema,
    AssignmentInterfaceSchema,
    AssignmentInterfaceAssignedSchema,
    AssignmentStatisticsOperatorSchema,
    AssignmentStatisticsSchema,
    UpdateStatusAssignmentBody,
    ReassignBody,
    RegisterAssignmentBody,
    RegisterAutoAssignment
)
from schemas.config import (
    SettingSchema,
    UserPermissionSchema,
    ChangeNotificationSchema
)
from schemas.change import (
    ChangeSchema,
    ChangeInterfaceSchema,
    RegisterChangeBody
)
from schemas.json import (
    JSONSettingSchema,
    JSONChangeNotificacionSchema,
    ChangeJsonSchema
)
