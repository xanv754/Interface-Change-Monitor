from typing import Annotated
from fastapi import APIRouter, Depends
from api import error
from core import SecurityCore
from controllers import SystemController
from schemas import OperatorSchema

router = APIRouter()


@router.get(f"/")
async def get_config(
    user: Annotated[OperatorSchema, Depends(SecurityCore.get_access_user)],
):
    """Get the settings of the system."""
    if not user:
        raise error.UNATHORIZED_USER
    config = SystemController.get_system_config()
    if config:
        return config.model_dump()
    else:
        raise error.CONFIG_SYSTEM