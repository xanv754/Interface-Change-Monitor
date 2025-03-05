from typing import Annotated
from fastapi import APIRouter, Depends, Query
from api import error, prefix
from constants import ProfileType
from controllers import OperatorController
from core import SecurityCore, SystemConfig
from schemas import OperatorResponseSchema, AssignmentInterfaceResponseSchema


router = APIRouter()
system = SystemConfig()
configuration = system.get_system_config()


@router.get(f"/{prefix.HISTORY_INFO}/me", response_model=list[AssignmentInterfaceResponseSchema])
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


@router.get(f"/{prefix.HISTORY_INFO}", response_model=list[AssignmentInterfaceResponseSchema])
async def get_assignments_revised_by_operator(
    user: Annotated[OperatorResponseSchema, Depends(SecurityCore.get_access_user)],
    username: str = Query(...),
):
    """Get all assignments revised of the user.

    **Query params**
    - username: Username of the operator.
    """
    if not user:
        raise error.UNATHORIZED_USER
    if ((user.profile == ProfileType.ROOT.value and not configuration.viewAllStatistics.ROOT) or
        (user.profile == ProfileType.ADMIN.value and not configuration.viewAllStatistics.ADMIN) or
        (user.profile == ProfileType.STANDARD.value and not configuration.viewAllStatistics.STANDARD) or
        (user.profile == ProfileType.SOPORT.value and not configuration.viewAllStatistics.SOPORT)
    ):
        raise error.UNATHORIZED_USER
    assignments = OperatorController.get_all_revised_assignments_by_operator(username)
    return [assignment.model_dump() for assignment in assignments]


@router.get(f"/{prefix.HISTORY_INFO}/all", response_model=list[AssignmentInterfaceResponseSchema])
async def get_all_assignments_revised(
    user: Annotated[OperatorResponseSchema, Depends(SecurityCore.get_access_user)],
):
    """Get all assignments revised in the system."""
    if not user:
        raise error.UNATHORIZED_USER
    if ((user.profile == ProfileType.ROOT.value and not configuration.viewAllStatistics.ROOT) or
        (user.profile == ProfileType.ADMIN.value and not configuration.viewAllStatistics.ADMIN) or
        (user.profile == ProfileType.STANDARD.value and not configuration.viewAllStatistics.STANDARD) or
        (user.profile == ProfileType.SOPORT.value and not configuration.viewAllStatistics.SOPORT)
    ):
        raise error.UNATHORIZED_USER
    assignments = OperatorController.get_all_assignments_revised()
    return assignments
