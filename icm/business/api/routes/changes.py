from typing import Annotated, Tuple
from fastapi import APIRouter, Depends
from icm.business.libs.code import ResponseCode
from icm.business.controllers.change import ChangeController
from icm.business.controllers.config import ConfigController
from icm.business.controllers.security import SecurityController
from icm.business.models.change import PaginatedChanges
from icm.business.models.user import UserModel


router = APIRouter()


@router.get("/changes", response_model=PaginatedChanges)
def get_changes(
    user: Annotated[UserModel, Depends(SecurityController.get_current_user)],
    page: int = 1,
    page_size: int = 100,
):
    """Get interfaces with changes of the day."""
    if not user:
        raise ResponseCode(status=401, message="User unauthorized").error
    permission_request = ConfigController.can_assign_permission(role=user.role)
    if not permission_request:
        raise ResponseCode(
            status=403, message="User not authorized to get interface changes"
        ).error
    controller = ChangeController()
    response: Tuple[ResponseCode, dict] = controller.get_interfaces_with_changes(
        page=page, page_size=page_size
    )
    if response[0].status == 200:
        return response[1]
    raise response[0].error
