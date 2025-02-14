from typing import Annotated
from fastapi import APIRouter, Depends
from api import OPERATOR_NOT_FOUND, ASSIGNMENT_NOT_FOUND
from controllers import OperatorController
from core import SecurityCore
from schemas import OperatorSchema, OperatorUpdateBody, OperatorUpdatePassword, AssignmentSchema, AssignmentUpdateStatus

router = APIRouter()

@router.get("/info", response_model=OperatorSchema)
async def get_operator(user: Annotated[OperatorSchema, Depends(SecurityCore.get_access_user)]):
    operator = OperatorController.get_operator(user.username)
    if operator:
        return operator.model_dump()
    else:
        raise OPERATOR_NOT_FOUND
    
@router.get("/assignments/pending", response_model=list[AssignmentSchema])
async def get_assignments_pending(user: Annotated[OperatorSchema, Depends(SecurityCore.get_access_user)]):
    assignments = OperatorController.get_assignments_pending(user.username)
    return assignments

@router.get("/assignments/all", response_model=list[AssignmentSchema])
async def get_assignments(user: Annotated[OperatorSchema, Depends(SecurityCore.get_access_user)]):
    assignments = OperatorController.get_all_assignments(user.username)
    return assignments

@router.put("/assignments/status")
async def update_assignment_status(
    user: Annotated[OperatorSchema, Depends(SecurityCore.get_access_user)], 
    body: AssignmentUpdateStatus
):
    status = OperatorController.update_status_assignment(body.id, body.new_status)
    if status:
        return {"message": "Assignment status updated"}
    else:
        raise ASSIGNMENT_NOT_FOUND
    
@router.patch("/info")
async def update_operator(
    user: Annotated[OperatorSchema, Depends(SecurityCore.get_access_user)], 
    body: OperatorUpdateBody
):
    status = OperatorController.update_operator(body)
    if status:
        return {"message": "Operator updated"}
    else:
        raise OPERATOR_NOT_FOUND
    
@router.put("/info/password")
async def update_operator_password(
    user: Annotated[OperatorSchema, Depends(SecurityCore.get_access_user)], 
    body: OperatorUpdatePassword
):
    status = OperatorController.update_password(user.username, body.password)
    if status:
        return {"message": "Password updated"}
    else:
        raise OPERATOR_NOT_FOUND