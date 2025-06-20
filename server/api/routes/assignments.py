from typing import Tuple
from fastapi import APIRouter
from controllers.assignment import AssignmentController
from constants.code import ResponseCode
from models.assignment import NewAssignmentModel, AssignmentModel


router = APIRouter()

@router.post("/assignments", status_code=201)
def new_assignments(assignments: list[NewAssignmentModel]):
    """New assignments."""
    controller = AssignmentController()
    response: ResponseCode = controller.new_assignment(assignments=assignments)
    if response.status == 201:
        return {"message": "Assignments created successfully"}
    raise response.error

@router.get("/assignments", response_model=list[AssignmentModel])
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