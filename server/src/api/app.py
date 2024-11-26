from fastapi import FastAPI
from api.routes.operator import router as operator  
from api.routes.assigment import router as assigment

app = FastAPI()

app.include_router(operator)
app.include_router(assigment)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app:app", host="0.0.0.0", port=8000)