from typing import Annotated, List
from fastapi import APIRouter, Depends, Query
from api import error, prefix
from constants import ProfileType
from controllers import OperatorController
from core import SecurityCore, SystemConfig
from schemas import OperatorResponseSchema, AssignmentInterfaceResponseSchema, AssignmentInterfaceAssignedResponseSchema


router = APIRouter()
system = SystemConfig()
configuration = system.get_system_config()


@router.get(f"/{prefix.HISTORY_INFO}/me", response_model=List[AssignmentInterfaceResponseSchema])
async def get_assignments_revised(
    user: Annotated[OperatorResponseSchema, Depends(SecurityCore.get_access_user)],
):
    """Get all assignments revised of the user who is logged in."""
    if not user:
        raise error.UNATHORIZED_USER
    assignments = OperatorController.get_all_revised_assignments_by_operator(
        user.username
    )
    return [assignment.model_dump() for assignment in assignments]


@router.get(f"/{prefix.HISTORY_INFO}", response_model=List[AssignmentInterfaceAssignedResponseSchema])
async def get_assignments_revised_by_month(
    user: Annotated[OperatorResponseSchema, Depends(SecurityCore.get_access_user)],
    month: int = Query(...)
):
    """Get all assignments revised by a month.

    **Query params**
    - month: Month to get the assignments revised.
    """
    if not user:
        raise error.UNATHORIZED_USER
    if ((user.profile == ProfileType.ROOT.value and not configuration.systemInformation.ROOT) or
        (user.profile == ProfileType.ADMIN.value and not configuration.systemInformation.ADMIN) or
        (user.profile == ProfileType.STANDARD.value and not configuration.systemInformation.STANDARD) or
        (user.profile == ProfileType.SOPORT.value and not configuration.systemInformation.SOPORT)
    ):
        raise error.UNATHORIZED_USER
    assignments = OperatorController.get_all_revised_assignments_operator_by_month(month)
    return [assignment.model_dump() for assignment in assignments]


@router.get(f"/{prefix.HISTORY_INFO}/all", response_model=List[AssignmentInterfaceResponseSchema])
async def get_all_assignments_revised(
    user: Annotated[OperatorResponseSchema, Depends(SecurityCore.get_access_user)],
):
    """Get all assignments revised in the system."""
    if not user:
        raise error.UNATHORIZED_USER
    if ((user.profile == ProfileType.ROOT.value and not configuration.systemInformation.ROOT) or
        (user.profile == ProfileType.ADMIN.value and not configuration.systemInformation.ADMIN) or
        (user.profile == ProfileType.STANDARD.value and not configuration.systemInformation.STANDARD) or
        (user.profile == ProfileType.SOPORT.value and not configuration.systemInformation.SOPORT)
    ):
        raise error.UNATHORIZED_USER
    assignments = OperatorController.get_all_assignments_revised()
    return assignments
