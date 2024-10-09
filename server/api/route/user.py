from fastapi import APIRouter, Depends, HTTPException, status
from models.autoAssignment import AutoAssignment
from models.assing import AssigmentStatusModel
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

@router.get("/api/v1/myuser")
def read_data_user(current_user: Annotated[dict, Depends(get_current_user)]):
    if current_user: 
        return current_user
    else: raise credentials_exception

@router.get("/api/v1/users/all")
def read_all_users(current_user: Annotated[dict, Depends(get_current_user)]):
    if current_user and current_user['type'] == usertype.admin:
        return Manager.get_users()
    else: raise credentials_exception

@router.get("/api/v1/users")
def read_users(current_user: Annotated[dict, Depends(get_current_user)]):
    if current_user: 
        return Manager.get_type_users()
    else: raise credentials_exception

@router.get("/api/v1/users/username={username}")
def read_user(username: str, current_user: Annotated[dict, Depends(get_current_user)]):
    if current_user:
        res = Manager.get_user(username)
        if not res: raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
        else: return res
    else: raise credentials_exception

@router.get("/api/v1/users/admin")
def read_users(current_user: Annotated[dict, Depends(get_current_user)]):
    if current_user and current_user['type'] == usertype.admin:
        return Manager.get_type_admin()
    else: raise credentials_exception

@router.get("/api/v1/users/pending")
def read_users_pending(current_user: Annotated[dict, Depends(get_current_user)]):
    if current_user and current_user['type'] == usertype.admin:
        return Manager.get_users_pending()
    else: raise credentials_exception

@router.get("/api/v1/users/admin/username={username}")
def read_user(username: str, current_user: Annotated[dict, Depends(get_current_user)]):
    if current_user and current_user['type'] == usertype.admin:
        res = Manager.get_admin(username)
        if not res: raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
        else: return res
    else: raise credentials_exception

@router.put("/api/v1/users/username={username}/status={user_status}")
def acceptance_user(username: str, user_status: str, current_user: Annotated[dict, Depends(get_current_user)]):
    if current_user and current_user['type'] == usertype.admin:
        res = Manager.update_status_user(username, user_status)
        if not res: raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
        else: return {"message": "User enabled"}
    else: raise credentials_exception

@router.delete("/api/v1/users/username={username}")
def delete_user(username: str, current_user: Annotated[dict, Depends(get_current_user)]):
    if current_user and current_user['type'] == usertype.admin:
        res = Manager.delete_user(username)
        if not res: raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
        else: return {"message": "User deleted"}
    else: raise credentials_exception

@router.put("/api/v1/users/autoAssignment", status_code=status.HTTP_204_NO_CONTENT)
def add_auto_assignment(current_user: Annotated[dict, Depends(get_current_user)], data: AutoAssignment):
    if current_user and current_user['type'] == usertype.admin:
        res = Manager.update_auto_assignment(data.usernames)
        if res: return
        else: raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Fail to auto assignment")
    else: raise credentials_exception

@router.put("/api/v1/users/assigned={username}/element={id_element}")
def add_assign_element(username: str, id_element: str, current_user: Annotated[dict, Depends(get_current_user)]):
    if current_user and current_user['type'] == usertype.admin:
        res = Manager.update_assign_element(username, id_element)
        if not res: raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
        else: return {"message": "Assignment status updated"}
    else: raise credentials_exception

@router.put("/api/v1/users/reviewed")
def update_assignment(data: AssigmentStatusModel, current_user: Annotated[dict, Depends(get_current_user)]):
    if current_user:
        res = Manager.update_assignment(data.username, data.idElement, data.status)
        if not res: raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Bad requests")
        else: return {"message": "Assignment status updated"}
    else: raise credentials_exception

@router.put("/api/v1/users/username={username}/name={new_name}")
def updated_name(username: str, new_name: str, current_user: Annotated[dict, Depends(get_current_user)]):
    if current_user:
        res = Manager.update_user_name(username, new_name)
        if not res: raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
        else: return {"message": "User updated"}
    else: raise credentials_exception

@router.put("/api/v1/users/username={username}/lastname={new_lastname}")
def updated_lastname(username: str, new_lastname: str, current_user: Annotated[dict, Depends(get_current_user)]):
    if current_user:
        res = Manager.update_user_lastname(username, new_lastname)
        if not res: raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
        else: return {"message": "User updated"}
    else: raise credentials_exception

@router.put("/api/v1/users/username={username}/password={new_password}")
def updated_password(username: str, new_password: str, current_user: Annotated[dict, Depends(get_current_user)]):
    if current_user:
        res = Manager.update_user_password(username, new_password)
        if not res: raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
        else: return {"message": "User updated"}
    else: raise credentials_exception

@router.put("/api/v1/users/username={username}/permission={permissionStatus}", status_code=status.HTTP_204_NO_CONTENT)
def change_forgotten_password(username: str, permissionStatus: str, current_user: Annotated[dict, Depends(get_current_user)]):
    if current_user and current_user['type'] == usertype.admin:
        res = Manager.permission_change_password(username, permissionStatus)
        if not res: raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="User not updated")
        else: return
    else: raise credentials_exception