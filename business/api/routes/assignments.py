from typing import Annotated
from fastapi import APIRouter, Depends
from pydantic import BaseModel
from business.libs.code import ResponseCode
from business.controllers.assignment import AssignmentController
from business.controllers.config import ConfigController
from business.controllers.security import SecurityController
from business.models.user import UserModel
from business.models.assignment import NewAssignmentModel, ReassignmentModel, UpdateAssignmentModel


router = APIRouter()

class RequestAutomaticAssignment(BaseModel):
    usernames: list[str]


@router.post("/assignments/new", status_code=201)
def new_assignments(assignments: list[NewAssignmentModel], user: Annotated[UserModel, Depends(SecurityController.get_current_user)]):
    """New assignments."""
    if not user:
        raise ResponseCode(status=401, message="User unauthorized").error
    permission_request = ConfigController.can_assign_permission(role=user.role)
    if not permission_request:
        raise ResponseCode(status=403, message="User not authorized to assign").error
    controller = AssignmentController()
    response: ResponseCode = controller.new_assignment(assignments=assignments)
    if response.status == 201:
        return {"message": "Assignments created successfully"}
    raise response.error

@router.post("/assignments/reassign")
def reassign_assignments(assignments: list[ReassignmentModel], user: Annotated[UserModel, Depends(SecurityController.get_current_user)]):
    """Reassign assignments."""
    if not user:
        raise ResponseCode(status=401, message="User unauthorized").error
    permission_request = ConfigController.can_assign_permission(role=user.role)
    if not permission_request:
        raise ResponseCode(status=403, message="User not authorized to reassign").error
    controller = AssignmentController()
    response: ResponseCode = controller.reassign(assignments=assignments)
    if response.status == 200:
        return {"message": "Assignments reassigned successfully"}
    raise response.error

@router.post("/assignments/automatic", status_code=201)
def automatic_assignment(request: RequestAutomaticAssignment, user: Annotated[UserModel, Depends(SecurityController.get_current_user)]):
    """Automatic assignment."""
    if not user:
        raise ResponseCode(status=401, message="User unauthorized").error
    permission_request = ConfigController.can_assign_permission(role=user.role)
    if not permission_request:
        raise ResponseCode(status=403, message="User not authorized to automatic assignment").error
    controller = AssignmentController()
    response: ResponseCode = controller.automatic_assignment(assign_by=user.username, usernames=request.usernames)
    if response.status == 201:
        return {"message": "Assignments automatic assigned successfully"}
    raise response.error

@router.post("/assignments/status")
def update_assignments_status(assignments: list[UpdateAssignmentModel], user: Annotated[UserModel, Depends(SecurityController.get_current_user)]):
    """Update assignments status."""
    if not user:
        raise ResponseCode(status=401, message="User unauthorized").error
    controller = AssignmentController()
    response: ResponseCode = controller.update_status_assignment(assignments=assignments, username=user.username)
    if response.status == 200:
        return {"message": "Assignments status updated successfully"}
    raise response.error