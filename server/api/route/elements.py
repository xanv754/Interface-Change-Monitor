from fastapi import APIRouter, Depends, HTTPException, status
from modules.security import get_current_user
from constants.userType import usertype
from modules.manager import Manager
from typing import Annotated

router = APIRouter()

credentials_exception = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Incorrect username or password", 
    headers={"WWW-Authenticate": "Bearer"},
)

@router.get("/api/v1/elements/backup")
def read_elements(current_user: Annotated[dict, Depends(get_current_user)]):
    if current_user:
        return Manager.get_elements_backup()
    else: raise credentials_exception

@router.get("/api/v1/elements")
def read_elements(current_user: Annotated[dict, Depends(get_current_user)]):
    if current_user and current_user['type'] == usertype.admin:
        return Manager.get_elements()
    else: raise credentials_exception

@router.get("/api/v1/elements/id={id}")
def read_elements(id: str, current_user: Annotated[dict, Depends(get_current_user)]):
    if current_user:
        if id:
            res = Manager.get_element(id)
            if not res: raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
            else: return res
        else:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="ID required")
    else: raise credentials_exception