from schemas.requests.post import (
    EquipmentRegisterBody,
    AssignmentRegisterBody,
    OperatorRegisterBody,
    InterfaceRegisterBody,
)
from schemas.requests.patch import (
    AssignmentUpdateStatus,
    OperatorUpdatePassword,
    AssignmentReassignBody,
    OperatorUpdateProfile,
    OperatorUpdateAccount,
)
from schemas.requests.put import OperatorUpdateBody, OperatorUpdateStandardBody
from schemas.data import TokenData
from schemas.responses.token import TokenResponse
from schemas.responses.assignment import StatisticsAssignmentResponse
from schemas.responses.data.operator import OperatorResponseSchema
from schemas.responses.data.equipment import EquipmentResponseSchema
from schemas.responses.data.interface import InterfaceResponseSchema
from schemas.responses.data.assignment import AssignmentResponseSchema, AssignmentInterfaceResponseSchema
from schemas.responses.config import SystemConfigResponse, SystemConfigUserSchema, SystemConfigNotificationSchema
from schemas.responses.changes import ChangesResponse, OldInterfaceSchema, NewInterfaceSchema
from schemas.responses.operator import OperatorResponse
from schemas.json import SystemConfigJson, SystemConfigNotificationJson, ChangesJson
