from typing import Annotated
from fastapi import APIRouter, Depends
from api import error
from controllers import SystemController, SecurityController
from schemas import OperatorSchema, SettingSchema

router = APIRouter()


@router.get(f"/", response_model=SettingSchema)
async def get_config(
    user: Annotated[OperatorSchema, Depends(SecurityController.get_access_user)],
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
    user: Annotated[OperatorSchema, Depends(SecurityController.get_access_root)],
    config: SettingSchema
):
    """Update the settings of the system."""
    if not user:
        raise error.UNATHORIZED_USER
    status = SystemController.update_config(config)
    if status:
        return {"message": "Settings updated"}
    else:
        raise error.CONFIG_SYSTEM
