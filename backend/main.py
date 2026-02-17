from fastapi import FastAPI
from utils.fast_connection import router

app = FastAPI()

@app.get("/")
def root():
    return {"Hello": "World"}

app.include_router(router)