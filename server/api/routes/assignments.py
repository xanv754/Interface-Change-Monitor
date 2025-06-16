from typing import Tuple
from fastapi import APIRouter
from controllers.assignment import AssignmentController
from constants.code import ResponseCode


router = APIRouter()


@router.get("/assignments")
def get_assignments():
    """Get assignments."""
    controller = AssignmentController()
    response: Tuple[ResponseCode, list] = controller.get_all_assignments_filter_by_status(status="PENDING")
    if response[0].status == 200:
        return response[1]
    raise response[0].error

@router.get("/assignments/statistics")
def get_assignments_statistics():
    """Get assignments statistics."""
    controller = AssignmentController()
    response: Tuple[ResponseCode, list] = controller.get_statistics_assignments(usernames=["unittest"])
    if response[0].status == 200:
        return response[1]
    raise response[0].error