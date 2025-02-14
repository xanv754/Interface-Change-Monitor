from typing import Annotated
from fastapi import APIRouter, Depends, Query
from api import error, prefix
from controllers import OperatorController
from core import SecurityCore
from schemas import OperatorSchema, AssignmentsCountResponse


router = APIRouter()


@router.get(f"/{prefix.STATISTICS_INFO}/me", response_model=AssignmentsCountResponse)
async def get_statistics(user: Annotated[OperatorSchema, Depends(SecurityCore.get_access_user)]):
    """Get statistics of the user who is logged in."""
    if not user:
        raise error.UNATHORIZED_USER
    statistics = OperatorController.get_total_assignments_by_operator(user.username)
    if not statistics:
        raise error.STATISTICS
    return statistics

@router.get(f"/{prefix.STATISTICS_INFO}", response_model=AssignmentsCountResponse)
async def get_statistics_by_operator(
    user: Annotated[OperatorSchema, Depends(SecurityCore.get_access_admin)],
    username: str = Query(...)
):
    """Get statistics of the user.

    **Query params**
    - username: Username of the operator.
    """
    if not user:
        raise error.UNATHORIZED_USER
    statistics = OperatorController.get_total_assignments_by_operator(username)
    if not statistics:
        raise error.STATISTICS
    return statistics

@router.get(f"/{prefix.STATISTICS_INFO}/all", response_model=AssignmentsCountResponse)
async def get_all_statistics(user: Annotated[OperatorSchema, Depends(SecurityCore.get_access_admin)]):
    """Get statistics of the all users."""
    if not user:
        raise error.UNATHORIZED_USER
    statistics = OperatorController.get_total_assignments()
    if not statistics:
        raise error.STATISTICS
    return statistics
