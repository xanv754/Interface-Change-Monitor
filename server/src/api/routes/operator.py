from typing import Annotated, List
from fastapi import APIRouter, Depends
from api import error, prefix
from constants import ProfileType
from controllers import OperatorController
from core import SecurityCore, SystemConfig
from schemas import (
    OperatorResponseSchema,
    OperatorResponse,
    OperatorUpdateBody,
    OperatorUpdateStandardBody,
    OperatorUpdatePassword,
    AssignmentResponseSchema,
    AssignmentUpdateStatus,
)

router = APIRouter()
system = SystemConfig()
configuration = system.get_system_config()

@router.get(f"/{prefix.OPERATOR_INFO}", response_model=OperatorResponse)
async def get_operator(
    user: Annotated[OperatorResponseSchema, Depends(SecurityCore.get_access_user)],
):
    """Get data of the user who is logged in."""
    if not user:
        raise error.UNATHORIZED_USER
    operator = OperatorController.get_operator(user.username)
    if operator:
        data = OperatorResponse(
            username=operator.username,
            name=operator.name,
            lastname=operator.lastname,
            profile=operator.profile,
            account=operator.account,
            createdAt=operator.createdAt,
            configuration=configuration
        )
        return data.model_dump()
    else: 
        raise error.OPERATOR_NOT_FOUND


@router.get(f"/{prefix.OPERATOR_ASSIGMENT}/all", response_model=list[AssignmentResponseSchema])
async def get_assignments(
    user: Annotated[OperatorResponseSchema, Depends(SecurityCore.get_access_user)],
):
    """Get all assignments of the user who is logged in."""
    if not user:
        raise error.UNATHORIZED_USER
    if ((user.profile == ProfileType.ROOT.value and not configuration.canReceiveAssignment.ROOT) or
        (user.profile == ProfileType.ADMIN.value and not configuration.canReceiveAssignment.ADMIN) or
        (user.profile == ProfileType.STANDARD.value and not configuration.canReceiveAssignment.STANDARD) or
        (user.profile == ProfileType.SOPORT.value and not configuration.canReceiveAssignment.SOPORT)
    ):
        raise error.UNATHORIZED_USER
    assignments = OperatorController.get_all_assignments_by_operator(user.username)
    return assignments


@router.get(
    f"/{prefix.OPERATOR_ASSIGMENT}/pending", response_model=list[AssignmentResponseSchema]
)
async def get_assignments_pending(
    user: Annotated[OperatorResponseSchema, Depends(SecurityCore.get_access_user)],
):
    """Get all assignments pending of the user who is logged in."""
    if not user:
        raise error.UNATHORIZED_USER
    if ((user.profile == ProfileType.ROOT.value and not configuration.canReceiveAssignment.ROOT) or
        (user.profile == ProfileType.ADMIN.value and not configuration.canReceiveAssignment.ADMIN) or
        (user.profile == ProfileType.STANDARD.value and not configuration.canReceiveAssignment.STANDARD) or
        (user.profile == ProfileType.SOPORT.value and not configuration.canReceiveAssignment.SOPORT)
    ):
        raise error.UNATHORIZED_USER
    assignments = OperatorController.get_all_assignments_pending_by_operator(
        user.username
    )
    return assignments


@router.put(f"/{prefix.OPERATOR_INFO}")
async def update_operator(
    user: Annotated[OperatorResponseSchema, Depends(SecurityCore.get_access_user)],
    body: OperatorUpdateStandardBody,
):
    """Update data of the user who is logged in.

    **Request body**
    - name: Name of the user
    - lastname: Lastname of the user
    """
    if not user:
        raise error.UNATHORIZED_USER    
    print(f"Usuario: ", user, "Body: ", body)
    schema = OperatorUpdateBody(
        username=user.username,
        name=body.name,
        lastname=body.lastname,
        profile=user.profile,
        account=user.account,
    )
    status = OperatorController.update_operator(schema)
    if status:
        return {"message": "Operator updated"}
    else:
        raise error.UPDATE_OPERATOR


@router.patch(f"/{prefix.OPERATOR_INFO}/password")
async def update_operator_password(
    user: Annotated[OperatorResponseSchema, Depends(SecurityCore.get_access_user)],
    body: OperatorUpdatePassword,
):
    """Update password of the user who is logged in.

    **Request Body**
    - password: The new password.
    """
    if not user:
        raise error.UNATHORIZED_USER
    status = OperatorController.update_password(user.username, body.password)
    if status:
        return {"message": "Password updated"}
    else:
        raise error.UPDATE_OPERATOR


@router.patch(f"/{prefix.OPERATOR_ASSIGMENT}/pending/status")
async def update_assignment_status_pending(
    user: Annotated[OperatorResponseSchema, Depends(SecurityCore.get_access_user)],
    body: List[AssignmentUpdateStatus],
):
    """Allow to update the status of an assignment pending.

    **Request body**
    - idAssignment: ID of the assignment to update
    - newStatus: New status of the assignment
    """
    if not user:
        raise error.UNATHORIZED_USER
    if ((user.profile == ProfileType.ROOT.value and not configuration.canReceiveAssignment.ROOT) or
        (user.profile == ProfileType.ADMIN.value and not configuration.canReceiveAssignment.ADMIN) or
        (user.profile == ProfileType.STANDARD.value and not configuration.canReceiveAssignment.STANDARD) or
        (user.profile == ProfileType.SOPORT.value and not configuration.canReceiveAssignment.SOPORT)
    ):
        raise error.UNATHORIZED_USER
    status = OperatorController.update_status_assignments_by_ids(body)
    if status:
        return {"message": "Assignment status updated"}
    else:
        raise error.UPDATE_STATUS_ASSIGNMENT
