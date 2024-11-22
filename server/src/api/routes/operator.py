from fastapi import APIRouter, Query
from database import OperatorController
from api.models.operator import OperatorBodyModel
from api.errors.operator import ErrorAPIOperatorHandler
from api.constant.delete import TypeDelete
from error import ErrorOperatorHandler

router = APIRouter(prefix="/api/v1")

@router.post("/operator/register")
def get_operators(body: OperatorBodyModel):
    res = OperatorController.create_operator(body.model_dump())
    if type(res) == ErrorOperatorHandler: 
        if res.code == 400: raise ErrorAPIOperatorHandler.BAD_REQUEST()
        elif res.code == 500: raise ErrorAPIOperatorHandler.UNKNOWN()
    else: return res

@router.get("/operator")
def get_operators():
    res = OperatorController.read_operators()
    if res is None: raise ErrorAPIOperatorHandler.UNKNOWN()
    return res

@router.get("/operator/all")
def get_operators():
    res = OperatorController.read_all_operators()
    if res is None: raise ErrorAPIOperatorHandler.UNKNOWN()
    return res

@router.get("/operator/username={username}")
def get_operators(username: str):
    if not username: raise ErrorAPIOperatorHandler.USERNAME_REQUIRED()
    res = OperatorController.read_operator(username)
    if not res and res == []: raise ErrorAPIOperatorHandler.NOT_FOUND()
    if res is None: raise ErrorAPIOperatorHandler.UNKNOWN()
    return res

@router.delete("/operator/")
def delete_operator(username: str = Query(None), delete: TypeDelete = Query(None)):
    # if not username: raise ErrorAPIOperatorHandler.USERNAME_REQUIRED()
    # if not delete: raise ErrorAPIOperatorHandler.BAD_REQUEST()
    # if delete == TypeDelete.HARD.value: 
    # elif delete == TypeDelete.SOFT.value: 
    #     # res = OperatorController.delete_operator_soft(username)
    #     pass
    # else: raise ErrorAPIOperatorHandler.BAD_REQUEST()
    res = OperatorController.delete_operator_hard(username)
    if type(res) == ErrorOperatorHandler: 
        print(res.code, res.message)
        if res.code == 10: raise ErrorAPIOperatorHandler.ERROR_CODE(404, res.message)
    else: return res