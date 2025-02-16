from typing import Annotated
from fastapi import APIRouter, Depends, Query
from api import error, prefix
from controllers import OperatorController
from core import SecurityCore
from schemas import OperatorSchema, AssignmentSchema


router = APIRouter()


@router.get(f"/{prefix.HISTORY_INFO}/me", response_model=list[AssignmentSchema])
async def get_assignments_revised(
    user: Annotated[OperatorSchema, Depends(SecurityCore.get_access_user)],
):
    """Get all assignments revised of the user who is logged in."""
    if not user:
        raise error.UNATHORIZED_USER
    assignments = OperatorController.get_all_assignments_revised_by_operator(
        user.username
    )
    return assignments


@router.get(f"/{prefix.HISTORY_INFO}", response_model=list[AssignmentSchema])
async def get_assignments_revised_by_operator(
    user: Annotated[OperatorSchema, Depends(SecurityCore.get_access_admin)],
    username: str = Query(...),
):
    """Get all assignments revised of the user.

    **Query params**
    - username: Username of the operator.
    """
    if not user:
        raise error.UNATHORIZED_USER
    assignments = OperatorController.get_all_assignments_revised_by_operator(username)
    return assignments


@router.get(f"/{prefix.HISTORY_INFO}/all", response_model=list[AssignmentSchema])
async def get_all_assignments_revised(
    user: Annotated[OperatorSchema, Depends(SecurityCore.get_access_admin)],
):
    """Get all assignments revised in the system."""
    if not user:
        raise error.UNATHORIZED_USER
    assignments = OperatorController.get_all_assignments_revised()
    return assignments
