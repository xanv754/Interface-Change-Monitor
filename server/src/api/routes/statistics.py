from typing import Annotated, List
from fastapi import APIRouter, Depends, Query
from api import error, prefix
from constants import ProfileType
from controllers import OperatorController
from core import SecurityCore, SystemConfig
from schemas import OperatorSchema, AssignmentStatisticsSchema


router = APIRouter()
system = SystemConfig()
configuration = system.get_system_config()

@router.get(f"/{prefix.STATISTICS_INFO}/me/all", response_model=AssignmentStatisticsSchema | None)
async def get_statistics(
    user: Annotated[OperatorSchema, Depends(SecurityCore.get_access_user)],
):
    """Get statistics of the user who is logged in."""
    if not user:
        raise error.UNATHORIZED_USER
    statistics = OperatorController.get_statistics_assignments_operator(operator=user.username)
    return statistics

@router.get(f"/{prefix.STATISTICS_INFO}/me/day", response_model=AssignmentStatisticsSchema | None)
async def get_statistics_by_day(
    user: Annotated[OperatorSchema, Depends(SecurityCore.get_access_user)],
    day: str = Query(...)
):
    """Get statistics of the user who is logged in on a specific day.
    
    Parameters
    -----------
    day : str
        Day to get the statistics.
    """
    if not user:
        raise error.UNATHORIZED_USER
    statistics = OperatorController.get_statistics_assignments_operator_by_day(operator=user.username, day=day)
    return statistics

@router.get(f"/{prefix.STATISTICS_INFO}/me/month", response_model=AssignmentStatisticsSchema | None)
async def get_statistics_by_month(
    user: Annotated[OperatorSchema, Depends(SecurityCore.get_access_user)],
    month: str = Query(...)
):
    """Get statistics of the user who is logged in on a specific month.
    
    Parameters
    -----------
    month : str
        Month to get the statistics.
    """
    if not user:
        raise error.UNATHORIZED_USER
    statistics = OperatorController.get_statistics_assignments_operator_by_month(operator=user.username, month=month)
    return statistics

@router.get(f"/{prefix.STATISTICS_INFO}/general/all", response_model=List[AssignmentStatisticsSchema])
async def get_all_statistics(
    user: Annotated[OperatorSchema, Depends(SecurityCore.get_access_user)],
):
    """Get statistics of the all users."""
    if not user:
        raise error.UNATHORIZED_USER
    if ((user.profile == ProfileType.ROOT.value and not configuration.systemInformation.ROOT) or
        (user.profile == ProfileType.ADMIN.value and not configuration.systemInformation.ADMIN) or
        (user.profile == ProfileType.STANDARD.value and not configuration.systemInformation.STANDARD) or
        (user.profile == ProfileType.SOPORT.value and not configuration.systemInformation.SOPORT)
    ):
        raise error.UNATHORIZED_USER
    statistics = OperatorController.get_statistics_assignments_general()
    return statistics

@router.get(f"/{prefix.STATISTICS_INFO}/general/day", response_model=List[AssignmentStatisticsSchema])
async def get_all_statistics_by_day(
    user: Annotated[OperatorSchema, Depends(SecurityCore.get_access_user)],
    day: str = Query(...)
):
    """Get statistics of the all users by an specific day.
    
    **Query params**
    - day: Day to get the statistics.
    """
    if not user:
        raise error.UNATHORIZED_USER
    if ((user.profile == ProfileType.ROOT.value and not configuration.systemInformation.ROOT) or
        (user.profile == ProfileType.ADMIN.value and not configuration.systemInformation.ADMIN) or
        (user.profile == ProfileType.STANDARD.value and not configuration.systemInformation.STANDARD) or
        (user.profile == ProfileType.SOPORT.value and not configuration.systemInformation.SOPORT)
    ):
        raise error.UNATHORIZED_USER
    statistics = OperatorController.get_statistics_assignments_general_by_day(day=day)
    return statistics

@router.get(f"/{prefix.STATISTICS_INFO}/general/month", response_model=List[AssignmentStatisticsSchema])
async def get_all_statistics_by_month(
    user: Annotated[OperatorSchema, Depends(SecurityCore.get_access_user)],
    month: str = Query(...)
):
    """Get statistics of the all users by an specific month.
    
    **Query params**
    - month: Day to get the statistics.
    """
    if not user:
        raise error.UNATHORIZED_USER
    if ((user.profile == ProfileType.ROOT.value and not configuration.systemInformation.ROOT) or
        (user.profile == ProfileType.ADMIN.value and not configuration.systemInformation.ADMIN) or
        (user.profile == ProfileType.STANDARD.value and not configuration.systemInformation.STANDARD) or
        (user.profile == ProfileType.SOPORT.value and not configuration.systemInformation.SOPORT)
    ):
        raise error.UNATHORIZED_USER
    statistics = OperatorController.get_statistics_assignments_general_by_month(month=month)
    return statistics