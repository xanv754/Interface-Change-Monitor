from typing import Annotated
from fastapi import APIRouter, Depends
from api import error
from core import SecurityCore
from controllers import SystemController
from schemas import OperatorResponseSchema, SystemConfigResponse

router = APIRouter()


@router.get(f"/")
async def get_config(
    user: Annotated[OperatorResponseSchema, Depends(SecurityCore.get_access_user)],
):
    """Get the settings of the system."""
    if not user:
        raise error.UNATHORIZED_USER
    config = SystemController.get_system_config()
    if config:
        return config.model_dump()
    else:
        raise error.CONFIG_SYSTEM
    
@router.put(f"/")
async def update_config(
    user: Annotated[OperatorResponseSchema, Depends(SecurityCore.get_access_root)],
    config: SystemConfigResponse
):
    """Update the settings of the system."""
    if not user:
        raise error.UNATHORIZED_USER
    status = SystemController.update_config(config)
    if status:
        return {"message": "Settings updated"}
    else:
        raise error.CONFIG_SYSTEM