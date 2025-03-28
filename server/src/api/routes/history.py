from typing import Annotated, List
from fastapi import APIRouter, Depends, Query
from api import error, prefix
from constants import ProfileType
from controllers import OperatorController, SecurityController
from system import SettingHandler
from schemas import OperatorSchema, AssignmentInterfaceSchema, AssignmentInterfaceAssignedSchema


router = APIRouter()
system = SettingHandler()
configuration = system.get_settings()


@router.get(f"/{prefix.HISTORY_INFO}/me", response_model=List[AssignmentInterfaceSchema])
async def get_assignments_revised(
    user: Annotated[OperatorSchema, Depends(SecurityController.get_access_user)],
):
    """Get all assignments revised of the user who is logged in."""
    if not user:
        raise error.UNATHORIZED_USER
    assignments = OperatorController.get_all_revised_assignments_by_operator(
        user.username
    )
    return [assignment.model_dump() for assignment in assignments]


@router.get(f"/{prefix.HISTORY_INFO}", response_model=List[AssignmentInterfaceAssignedSchema])
async def get_assignments_revised_by_month(
    user: Annotated[OperatorSchema, Depends(SecurityController.get_access_user)],
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
    assignments = OperatorController.get_all_revised_assignments_by_month(month)
    return [assignment.model_dump() for assignment in assignments]


@router.get(f"/{prefix.HISTORY_INFO}/all", response_model=List[AssignmentInterfaceSchema])
async def get_all_assignments_revised(
    user: Annotated[OperatorSchema, Depends(SecurityController.get_access_user)],
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
