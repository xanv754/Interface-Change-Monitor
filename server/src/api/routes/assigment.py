from fastapi import APIRouter, Query
from database import AssignmentController
from error import ErrorAssignmentHandler, CODEASSIGNMENT
from api.models.assignment import AssignmentBodyModel
from errors.error import ERROR_API

router = APIRouter(prefix="/api/v1")

@router.get('/operator/assignment/all')
def get_assignments(operator: str = Query(None)):
    if not operator:
        raise ERROR_API(ErrorAssignmentHandler(CODEASSIGNMENT.ERROR_400_USERNAME_REQUIRED))
    else:
        res = AssignmentController.read_assignments_by_operator(operator)
        if type(res) == ErrorAssignmentHandler: raise ERROR_API(res)
        else: return res

@router.get('/operator/assignment/pending')
def get_assignments_pending(operator: str = Query(None)):
    if not operator:
        raise ERROR_API(ErrorAssignmentHandler(CODEASSIGNMENT.ERROR_400_USERNAME_REQUIRED))
    else:
        res = AssignmentController.read_assignments_by_operator_pending(operator)
        if type(res) == ErrorAssignmentHandler: raise ERROR_API(res)
        else: return res

@router.get('/assignment/search')
def get_assignment(operator: str = Query(None), changeInterface: int = Query(None), oldInterface: int = Query(None)):
    if not changeInterface or not oldInterface:
        raise ERROR_API(ErrorAssignmentHandler(CODEASSIGNMENT.ERROR_400_ID_INTERFACE_REQUIRED))
    if not operator:
        raise ERROR_API(ErrorAssignmentHandler(CODEASSIGNMENT.ERROR_400_USERNAME_REQUIRED))
    res = AssignmentController.read_assignment_by_id(operator, changeInterface, oldInterface)
    if type(res) == ErrorAssignmentHandler: raise ERROR_API(res)
    else: return res

@router.get('/assignment/filter/date/assignment')
def get_assignments_by_date_assignment(date: str = Query(None)):
    if not date:
        raise ERROR_API(ErrorAssignmentHandler(CODEASSIGNMENT.ERROR_400_DATE_REQUIRED))
    else:
        res = AssignmentController.read_assignments_by_date_assignment(date)
        if type(res) == ErrorAssignmentHandler: raise ERROR_API(res)
        else: return res

@router.get('/assignment/filter/status')
def get_assignments_by_status(status: str = Query(None)):
    if not status:
        raise ERROR_API(ErrorAssignmentHandler(CODEASSIGNMENT.ERROR_400_STATUS_REQUIRED))
    else:
        res = AssignmentController.read_assignments_by_status(status)
        if type(res) == ErrorAssignmentHandler: raise ERROR_API(res)
        else: return res

@router.get('/assignment/filter/date/review')
def get_assignments_by_review(date: str = Query(None)):
    if not date:
        raise ERROR_API(ErrorAssignmentHandler(CODEASSIGNMENT.ERROR_400_DATE_REQUIRED))
    else:
        res = AssignmentController.read_assignments_by_review(date)
        if type(res) == ErrorAssignmentHandler: raise ERROR_API(res)
        else: return res

@router.post('/assignment/register')
def new_assignment(body: AssignmentBodyModel):
    res = AssignmentController.create_assignment(body.model_dump())
    if type(res) == ErrorAssignmentHandler: raise ERROR_API(res)
    else: return res

@router.delete('/assignment/delete/hard')
def delete_assignment(operator: str = Query(None), changeInterface: int = Query(None), oldInterface: int = Query(None)):
    if not operator:
        raise ERROR_API(ErrorAssignmentHandler(CODEASSIGNMENT.ERROR_400_USERNAME_REQUIRED))
    if not changeInterface or not oldInterface:
        raise ERROR_API(ErrorAssignmentHandler(CODEASSIGNMENT.ERROR_400_ID_INTERFACE_REQUIRED))
    res = AssignmentController.delete_assignment(operator, changeInterface, oldInterface)
    if type(res) == ErrorAssignmentHandler: raise ERROR_API(res)
    else: return res

@router.delete('/assignment/delete/hard/byDate/assignment')
def delete_assignment_by_date_assignment(date: str = Query(None)):
    if not date:
        raise ERROR_API(ErrorAssignmentHandler(CODEASSIGNMENT.ERROR_400_DATE_REQUIRED))
    res = AssignmentController.delete_assignments_by_date_assignment(date)
    if type(res) == ErrorAssignmentHandler: raise ERROR_API(res)
    else: return res

@router.patch('/assignment/change/status')
def update_assignment(operator: str = Query(None), changeInterface: int = Query(None), oldInterface: int = Query(None), status: str = Query(None)):
    if not operator:
        raise ERROR_API(ErrorAssignmentHandler(CODEASSIGNMENT.ERROR_400_USERNAME_REQUIRED))
    if not changeInterface or not oldInterface:
        raise ERROR_API(ErrorAssignmentHandler(CODEASSIGNMENT.ERROR_400_ID_INTERFACE_REQUIRED))
    if not status:
        raise ERROR_API(ErrorAssignmentHandler(CODEASSIGNMENT.ERROR_400_STATUS_REQUIRED))
    res = AssignmentController.update_status_assignment(changeInterface, oldInterface, operator, status)
    if type(res) == ErrorAssignmentHandler: raise ERROR_API(res)
    else: return res

@router.patch('/assignment/change/operator')
def update_operator_assignment(operator: str = Query(None), changeInterface: int = Query(None), oldInterface: int = Query(None), oldOperator: str = Query(None), assignedBy: str = Query(None)):
    if not operator or not oldOperator:
        raise ERROR_API(ErrorAssignmentHandler(CODEASSIGNMENT.ERROR_400_USERNAME_REQUIRED))
    if not changeInterface or not oldInterface:
        raise ERROR_API(ErrorAssignmentHandler(CODEASSIGNMENT.ERROR_400_ID_INTERFACE_REQUIRED))
    if not assignedBy:
        raise ERROR_API(ErrorAssignmentHandler(CODEASSIGNMENT.ERROR_400_NAME_REQUIRED))
    res = AssignmentController.update_operator_assingment(changeInterface, oldInterface, oldOperator, operator, assignedBy)
    if type(res) == ErrorAssignmentHandler: raise ERROR_API(res)
    else: return res