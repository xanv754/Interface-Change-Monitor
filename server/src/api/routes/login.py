from fastapi import APIRouter

router = APIRouter()

@router.get("/login")
def read_root():
    return {"message": "Iniciando sesión..."}