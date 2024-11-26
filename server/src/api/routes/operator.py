from fastapi import APIRouter, Query
from database import OperatorController
from error import ErrorOperatorHandler, STATUS
from api.models.operator import OperatorBodyModel
from api.constant.delete import TypeDelete
from api.errors.operator import ERROR_API

router = APIRouter(prefix="/api/v1")

@router.post("/operator/register")
def get_operators(body: OperatorBodyModel):
    res = OperatorController.create_operator(body.model_dump())
    if type(res) == ErrorOperatorHandler: raise ERROR_API(res)
    else: return res

@router.get("/operator")
def get_operators():
    res = OperatorController.read_operators()
    if type(res) == ErrorOperatorHandler: raise ERROR_API(res)
    else: return res

@router.get("/operator/all")
def get_operators():
    res = OperatorController.read_all_operators()
    if type(res) == ErrorOperatorHandler: raise ERROR_API(res)
    else: return res

@router.get("/operator/")
def get_operators(username: str = Query(None)):
    if not username: 
        error = ErrorOperatorHandler(STATUS.ERROR_400_USERNAME_REQUIRED)
        raise ERROR_API(error)
    res = OperatorController.read_operator(username)
    if type(res) == ErrorOperatorHandler: raise ERROR_API(res)
    else: return res

@router.delete("/operator/")
def delete_operator(username: str = Query(None), delete: TypeDelete = Query(None)):
    if not username: 
        error = ErrorOperatorHandler(STATUS.ERROR_400_USERNAME_REQUIRED)
        raise ERROR_API(error)
    if not delete: 
        error = ErrorOperatorHandler(STATUS.ERROR_400_OPTION_REQUIRED)
        raise ERROR_API(error)
    if delete == TypeDelete.HARD.value: 
        res = OperatorController.delete_operator_hard(username)
    elif delete == TypeDelete.SOFT.value: 
        res = OperatorController.delete_operator_soft(username)
    else: 
        error = ErrorOperatorHandler(STATUS.ERROR_400_DELETE_NOT_VALID)
        raise ERROR_API(error)
    if type(res) == ErrorOperatorHandler: 
        raise ERROR_API(res)
    else: return res