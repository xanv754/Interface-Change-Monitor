from fastapi import APIRouter, Query
from database import OperatorController
from error import ErrorOperatorHandler, CODEOPERATOR
from api.models.operator import OperatorBodyModel
from api.constant.delete import TypeDelete
from errors.error import ERROR_API

router = APIRouter(prefix="/api/v1")

@router.get("/operator/search/all")
def get_operators():
    res = OperatorController.read_operators()
    if type(res) == ErrorOperatorHandler: raise ERROR_API(res)
    else: return res

@router.get("/operator/search/all/v2")
def get_operators():
    res = OperatorController.read_all_operators()
    if type(res) == ErrorOperatorHandler: raise ERROR_API(res)
    else: return res

@router.get("/operator/search")
def get_operators(username: str = Query(None)):
    if not username: 
        error = ErrorOperatorHandler(CODEOPERATOR.ERROR_400_USERNAME_REQUIRED)
        raise ERROR_API(error)
    res = OperatorController.read_operator(username)
    if type(res) == ErrorOperatorHandler: raise ERROR_API(res)
    else: return res

@router.post("/operator/register")
def new_operator(body: OperatorBodyModel):
    res = OperatorController.create_operator(body.model_dump())
    if type(res) == ErrorOperatorHandler: raise ERROR_API(res)
    else: return res

@router.delete("/operator/delete/hard")
def delete_operator_hard(username: str = Query(None)):
    if not username: 
        error = ErrorOperatorHandler(CODEOPERATOR.ERROR_400_USERNAME_REQUIRED)
        raise ERROR_API(error)
    res = OperatorController.delete_operator_hard(username)
    if type(res) == ErrorOperatorHandler: 
        raise ERROR_API(res)
    else: return res

@router.delete("/operator/delete/soft")
def delete_operator_soft(username: str = Query(None)):
    if not username: 
        error = ErrorOperatorHandler(CODEOPERATOR.ERROR_400_USERNAME_REQUIRED)
        raise ERROR_API(error)
    res = OperatorController.delete_operator_soft(username)
    if type(res) == ErrorOperatorHandler: 
        raise ERROR_API(res)
    else: return res