from typing import Annotated
from fastapi import APIRouter, Depends, Query
from api import error, prefix
from constants import ProfileType
from controllers import OperatorController
from core import SecurityCore, SystemConfig
from schemas import OperatorResponseSchema, StatisticsAssignmentResponse


router = APIRouter()
system = SystemConfig()
configuration = system.get_system_config()

@router.get(f"/{prefix.STATISTICS_INFO}/me", response_model=StatisticsAssignmentResponse)
async def get_statistics(
    user: Annotated[OperatorResponseSchema, Depends(SecurityCore.get_access_user)],
):
    """Get statistics of the user who is logged in."""
    if not user:
        raise error.UNATHORIZED_USER
    statistics = OperatorController.get_statistics_assignments_by_operator(user.username)
    if not statistics:
        raise error.STATISTICS
    return statistics


@router.get(f"/{prefix.STATISTICS_INFO}", response_model=StatisticsAssignmentResponse)
async def get_statistics_by_operator(
    user: Annotated[OperatorResponseSchema, Depends(SecurityCore.get_access_user)],
    username: str = Query(...),
):
    """Get statistics of the user.

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
    statistics = OperatorController.get_statistics_assignments_by_operator(username)
    if not statistics:
        raise error.STATISTICS
    return statistics


@router.get(f"/{prefix.STATISTICS_INFO}/all", response_model=StatisticsAssignmentResponse)
async def get_all_statistics(
    user: Annotated[OperatorResponseSchema, Depends(SecurityCore.get_access_user)],
):
    """Get statistics of the all users."""
    if not user:
        raise error.UNATHORIZED_USER
    if ((user.profile == ProfileType.ROOT.value and not configuration.viewAllStatistics.ROOT) or
        (user.profile == ProfileType.ADMIN.value and not configuration.viewAllStatistics.ADMIN) or
        (user.profile == ProfileType.STANDARD.value and not configuration.viewAllStatistics.STANDARD) or
        (user.profile == ProfileType.SOPORT.value and not configuration.viewAllStatistics.SOPORT)
    ):
        raise error.UNATHORIZED_USER
    statistics = OperatorController.get_general_statistics_assignments()
    if not statistics:
        raise error.STATISTICS
    return statistics
