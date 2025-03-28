from typing import Annotated, List
from fastapi import APIRouter, Depends, Query
from api import error, prefix
from constants import ProfileType
from controllers import OperatorController, ChangeController, SecurityController
from system import SettingHandler
from schemas import (
    OperatorSchema,
    UpdateProfileBody,
    UpdateAccountBody,
    UpdateUserRootBody,
    RegisterAssignmentBody,
    ReassignBody,
    ChangeInterfaceSchema,
    RegisterAutoAssignment
)

router = APIRouter()
system = SettingHandler()
configuration = system.get_settings()

@router.get(f"/{prefix.ADMIN_CHANGES}", response_model=list[ChangeInterfaceSchema])
def get_changes(
    user: Annotated[OperatorSchema, Depends(SecurityController.get_access_user)],
):
    """Get all changes of the system."""
    if not user:
        raise error.UNATHORIZED_USER
    if ((user.profile == ProfileType.ROOT.value and not configuration.canAssign.ROOT) or
        (user.profile == ProfileType.ADMIN.value and not configuration.canAssign.ADMIN) or
        (user.profile == ProfileType.STANDARD.value and not configuration.canAssign.STANDARD) or
        (user.profile == ProfileType.SOPORT.value and not configuration.canAssign.SOPORT)
    ):
        raise error.UNATHORIZED_USER
    changes = ChangeController.get_all_changes()
    return changes


@router.post(f"/{prefix.ADMIN_ASSIGNMENT_INFO}/assign")
def add_assignment(
    user: Annotated[OperatorSchema, Depends(SecurityController.get_access_user)],
    body: List[RegisterAssignmentBody],
):
    """Allow to assign an interface to an operator for your review.

    **Request body**
    List of assignments to register.
        - idChange: ID of the change to assign.
        - change_interface: ID of the interface to assign in your new version.
        - old_interface: ID of the interface to assign in your old version.
        - operator: Operator to assign the interfaces.
        - assigned_by: Operator who assigned the interfaces.
    """
    if not user:
        raise error.UNATHORIZED_USER
    if ((user.profile == ProfileType.ROOT.value and not configuration.canAssign.ROOT) or
        (user.profile == ProfileType.ADMIN.value and not configuration.canAssign.ADMIN) or
        (user.profile == ProfileType.STANDARD.value and not configuration.canAssign.STANDARD) or
        (user.profile == ProfileType.SOPORT.value and not configuration.canAssign.SOPORT)
    ):
        raise error.UNATHORIZED_USER
    status = OperatorController.add_assignment(body)
    if status:
        return {"message": "Assignments added"}
    else:
        raise error.ASSIGN

@router.post(f"/{prefix.ADMIN_ASSIGNMENT_INFO}/autoassign")
def auto_assignment(
    user: Annotated[OperatorSchema, Depends(SecurityController.get_access_user)],
    body: List[RegisterAutoAssignment],
):
    """Allow to auto assign an interface to an operator for your review.

    **Request body**
    List of assignments to register.
        - users: List of usernames of the operators.
        - assigned_by: Operator who assigned the interfaces.
    """
    if not user:
        raise error.UNATHORIZED_USER
    if ((user.profile == ProfileType.ROOT.value and not configuration.canAssign.ROOT) or
        (user.profile == ProfileType.ADMIN.value and not configuration.canAssign.ADMIN) or
        (user.profile == ProfileType.STANDARD.value and not configuration.canAssign.STANDARD) or
        (user.profile == ProfileType.SOPORT.value and not configuration.canAssign.SOPORT)
    ):
        raise error.UNATHORIZED_USER
    status = OperatorController.auto_assignment(body)
    if status:
        return {"message": "Assignments added"}
    else:
        raise error.ASSIGN


@router.put(f"/{prefix.ADMIN_ASSIGNMENT_INFO}/reassign")
def update_reassign(
    user: Annotated[OperatorSchema, Depends(SecurityController.get_access_user)],
    body: List[ReassignBody],
):
    """Allow to reassign an assignment existing an other operator active.

    **Request body**
    - id_assignment: ID of the assignment to reassign.
    - new_operator: Operator to reassign the assignment.
    - assigned_by: Operator who assigned the assignment.
    """
    if not user:
        raise error.UNATHORIZED_USER
    if ((user.profile == ProfileType.ROOT.value and not configuration.canAssign.ROOT) or
        (user.profile == ProfileType.ADMIN.value and not configuration.canAssign.ADMIN) or
        (user.profile == ProfileType.STANDARD.value and not configuration.canAssign.STANDARD) or
        (user.profile == ProfileType.SOPORT.value and not configuration.canAssign.SOPORT)
    ):
        raise error.UNATHORIZED_USER
    status = OperatorController.reassignment(body)
    if status:
        return {"message": "Assignment reassigned"}
    else:
        raise error.ASSIGNMENT_NOT_FOUND


@router.get(
    f"/{prefix.ADMIN_OPERATOR_INFO}/info/all", response_model=list[OperatorSchema]
)
async def get_operators(
    user: Annotated[OperatorSchema, Depends(SecurityController.get_access_user)],
):
    """Get all operators (active and inactive) of the system."""
    if not user:
        raise error.UNATHORIZED_USER
    if ((user.profile == ProfileType.ROOT.value and not configuration.canAssign.ROOT) or
        (user.profile == ProfileType.ADMIN.value and not configuration.canAssign.ADMIN) or
        (user.profile == ProfileType.STANDARD.value and not configuration.canAssign.STANDARD) or
        (user.profile == ProfileType.SOPORT.value and not configuration.canAssign.SOPORT)
    ):
        raise error.UNATHORIZED_USER
    all_operators = OperatorController.get_operators()
    operators: List[OperatorSchema] = []
    for operator in all_operators:
        if operator.profile == ProfileType.ROOT.value and configuration.canReceiveAssignment.ROOT:
            operators.append(operator.model_dump())
        elif operator.profile == ProfileType.ADMIN.value and configuration.canReceiveAssignment.ADMIN:
            operators.append(operator.model_dump())
        elif operator.profile == ProfileType.STANDARD.value and configuration.canReceiveAssignment.STANDARD:
            operators.append(operator.model_dump())
        elif operator.profile == ProfileType.SOPORT.value and configuration.canReceiveAssignment.SOPORT:
            operators.append(operator.model_dump())
    return operators

@router.get(f"/{prefix.ADMIN_OPERATOR_INFO}/info", response_model=OperatorSchema)
async def get_operator(
    user: Annotated[OperatorSchema, Depends(SecurityController.get_access_root)],
    username: str = Query(...),
):
    """Get data of the operator with the given username.

    **Query params**
    - username: Username of the operator.
    """
    if not user:
        raise error.UNATHORIZED_USER
    operator = OperatorController.get_operator(username)
    if operator:
        return operator.model_dump()
    else:
        raise error.OPERATOR_NOT_FOUND


@router.patch(f"/{prefix.ADMIN_OPERATOR_INFO}/info/profile")
def update_operator_profile(
    user: Annotated[OperatorSchema, Depends(SecurityController.get_access_root)],
    body: UpdateProfileBody,
):
    """Allow to update the profile of an operator.

    **Request body**
    - username: Username of the operator.
    - profile: Profile type of the operator.
    """
    if not user:
        raise error.UNATHORIZED_USER
    operator = OperatorController.get_operator(body.username)
    if not operator:
        raise error.OPERATOR_NOT_FOUND
    schema = UpdateUserRootBody(
        username=operator.username,
        name=operator.name,
        lastname=operator.lastname,
        profile=body.profile,
        account=operator.account,
    )
    status = OperatorController.update_operator(schema)
    if status:
        return {"message": "Operator updated"}
    else:
        raise error.UPDATE_OPERATOR


@router.patch(f"/{prefix.ADMIN_OPERATOR_INFO}/info/account")
def update_operator_profile(
    user: Annotated[OperatorSchema, Depends(SecurityController.get_access_root)],
    body: UpdateAccountBody,
):
    """Allow to update the account of an operator.

    **Request body**
    - username: Username of the operator.
    - account: Account type of the operator.
    """
    if not user:
        raise error.UNATHORIZED_USER
    operator = OperatorController.get_operator(body.username)
    if not operator:
        raise error.OPERATOR_NOT_FOUND
    schema = UpdateUserRootBody(
        username=operator.username,
        name=operator.name,
        lastname=operator.lastname,
        profile=operator.profile,
        account=body.account,
    )
    status = OperatorController.update_operator(schema)
    if status:
        return {"message": "Operator updated"}
    else:
        raise error.UPDATE_OPERATOR


@router.delete(f"/{prefix.ADMIN_OPERATOR_INFO}")
def delete_operator(
    user: Annotated[OperatorSchema, Depends(SecurityController.get_access_root)],
    username: str = Query(...),
):
    """Allow to delete an operator.

    **Query params**
    - username: Username of the operator.
    """
    if not user:
        raise error.UNATHORIZED_USER
    status = OperatorController.delete_soft_operator(username)
    if status:
        return {"message": "Operator deleted"}
    else:
        raise error.DELETE_OPERATOR
