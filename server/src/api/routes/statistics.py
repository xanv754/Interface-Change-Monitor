from typing import Annotated, List
from fastapi import APIRouter, Depends, Query
from api import error, prefix
from constants import ProfileType
from controllers import OperatorController, SecurityController
from schemas import OperatorSchema, AssignmentStatisticsOperatorSchema, AssignmentStatisticsSchema
from manager import SettingHandler


router = APIRouter()
system = SettingHandler()
configuration = system.get_settings()

@router.get(f"/{prefix.STATISTICS_INFO}/me/all", response_model=AssignmentStatisticsOperatorSchema | None)
async def get_statistics(
    user: Annotated[OperatorSchema, Depends(SecurityController.get_access_user)],
):
    """Get statistics of the user who is logged in."""
    if not user:
        raise error.UNATHORIZED_USER
    statistics = OperatorController.get_statistics_assignments_operator(operator=user.username)
    return statistics

@router.get(f"/{prefix.STATISTICS_INFO}/me/day", response_model=AssignmentStatisticsOperatorSchema | None)
async def get_statistics_by_day(
    user: Annotated[OperatorSchema, Depends(SecurityController.get_access_user)],
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

@router.get(f"/{prefix.STATISTICS_INFO}/me/month", response_model=AssignmentStatisticsOperatorSchema | None)
async def get_statistics_by_month(
    user: Annotated[OperatorSchema, Depends(SecurityController.get_access_user)],
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

@router.get(f"/{prefix.STATISTICS_INFO}/general/day", response_model=AssignmentStatisticsSchema)
async def get_all_statistics_by_day(
    user: Annotated[OperatorSchema, Depends(SecurityController.get_access_user)],
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
    statistics = OperatorController.get_statistics_general_by_day(day=day)
    if statistics:
        return statistics
    else:
        raise error.STATISTICS_NOT_FOUND

@router.get(f"/{prefix.STATISTICS_INFO}/general/month", response_model=AssignmentStatisticsSchema)
async def get_all_statistics_by_month(
    user: Annotated[OperatorSchema, Depends(SecurityController.get_access_user)],
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
    statistics = OperatorController.get_statistics_general_by_month(month=month)
    if statistics:
        return statistics
    else:
        raise error.STATISTICS_NOT_FOUND

@router.get(f"/{prefix.STATISTICS_INFO}/general/operators/all", response_model=List[AssignmentStatisticsOperatorSchema])
async def get_all_statistics_operators(
    user: Annotated[OperatorSchema, Depends(SecurityController.get_access_user)]
):
    """Get statistics of the all users by an specific month."""
    if not user:
        raise error.UNATHORIZED_USER
    if ((user.profile == ProfileType.ROOT.value and not configuration.systemInformation.ROOT) or
        (user.profile == ProfileType.ADMIN.value and not configuration.systemInformation.ADMIN) or
        (user.profile == ProfileType.STANDARD.value and not configuration.systemInformation.STANDARD) or
        (user.profile == ProfileType.SOPORT.value and not configuration.systemInformation.SOPORT)
    ):
        raise error.UNATHORIZED_USER
    statistics = OperatorController.get_statistics_general_operators()
    return statistics

@router.get(f"/{prefix.STATISTICS_INFO}/general/operators/day", response_model=List[AssignmentStatisticsOperatorSchema])
async def get_all_statistics_operators_by_month(
    user: Annotated[OperatorSchema, Depends(SecurityController.get_access_user)],
    day: str = Query(...)
):
    """Get statistics of the all users by an specific month.

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
    statistics = OperatorController.get_statistics_general_operators_by_day(month=day)
    return statistics

@router.get(f"/{prefix.STATISTICS_INFO}/general/operators/month", response_model=List[AssignmentStatisticsOperatorSchema])
async def get_all_statistics_operators_by_month(
    user: Annotated[OperatorSchema, Depends(SecurityController.get_access_user)],
    month: str = Query(...)
):
    """Get statistics of the all users by an specific month.

    **Query params**
    - month: Month to get the statistics.
    """
    if not user:
        raise error.UNATHORIZED_USER
    if ((user.profile == ProfileType.ROOT.value and not configuration.systemInformation.ROOT) or
        (user.profile == ProfileType.ADMIN.value and not configuration.systemInformation.ADMIN) or
        (user.profile == ProfileType.STANDARD.value and not configuration.systemInformation.STANDARD) or
        (user.profile == ProfileType.SOPORT.value and not configuration.systemInformation.SOPORT)
    ):
        raise error.UNATHORIZED_USER
    statistics = OperatorController.get_statistics_general_operators_by_month(month=month)
    return statistics
