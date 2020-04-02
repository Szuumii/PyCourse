from fastapi import FastAPI
from pydantic import BaseModel
import json

app = FastAPI()

class HelloNameResp(BaseModel):
    message: str

class MethodResp(BaseModel):
    method: str


@app.get("/")
def root():
    return {"message": "Hello World during the coronavirus pandemic!"}


@app.get('/hello/{name}', response_model=HelloNameResp)
def hello_name(name: str):
    return HelloNameResp(message=f"Hello {name}")


@app.get("/method")
def method_GET():
    return MethodResp(method="GET")

@app.post("/method")
def method_GET():
    return MethodResp(method="POST")

@app.put("/method")
def method_GET():
    return MethodResp(method="PUT")

@app.delete("/method")
def method_GET():
    return MethodResp(method="DELETE")
