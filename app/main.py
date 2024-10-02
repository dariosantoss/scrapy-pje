from fastapi import FastAPI
from .routers import pjeRouter

app = FastAPI()

app.include_router(pjeRouter.router)

@app.get("/")
def read_root():
    return {"Hello": "World"}
