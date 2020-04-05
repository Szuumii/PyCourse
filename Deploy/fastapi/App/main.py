from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import json
from typing import Dict

app = FastAPI()
app.patient_list = []

class HelloNameResp(BaseModel):
    message: str

class MethodResp(BaseModel):
    method: str

class PatientRq(BaseModel):
    name: str
    surename: str

class PatientResp(BaseModel):
    id: int
    patient: Dict
    


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
def method_POST():
    return MethodResp(method="POST")

@app.put("/method")
def method_PUT():
    return MethodResp(method="PUT")

@app.delete("/method")
def method_DELETE():
    return MethodResp(method="DELETE")

@app.post("/patient", response_model=PatientResp)
def recieve_patient(req: PatientRq):
    app.patient_list.append(req.dict())
    return PatientResp(id = app.patient_list.index(req.dict()),patient=req.dict())

@app.get("/patient/{pk}",response_model=PatientRq)
def return_patient_under_id(pk: int):
    if (len(app.patient_list)-1) < pk:
        raise HTTPException(status_code=404, detail="Patient not found")
    return app.patient_list[pk]
