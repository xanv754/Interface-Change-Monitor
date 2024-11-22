from fastapi import FastAPI
from api.routes.operator import router as operator  

app = FastAPI()

app.include_router(operator)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app:app", host="0.0.0.0", port=8000)