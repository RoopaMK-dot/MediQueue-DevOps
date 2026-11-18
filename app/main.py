from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field

from app.queue_manager import (
    DOCTORS,
    call_next_patient,
    get_doctor_queue,
    get_patient,
    register_patient,
)

app = FastAPI(
    title="MediQueue – Smart Hospital Queue Manager",
    description="A student DevOps project demonstrating digital patient tokens and doctor-wise queues.",
    version="1.0.0",
)


class PatientCreate(BaseModel):
    name: str = Field(min_length=2, max_length=80)
    age: int = Field(ge=0, le=120)
    doctor_id: int


@app.get("/", tags=["General"])
def home():
    return {"message": "Welcome to MediQueue", "docs": "/docs"}


@app.get("/health", tags=["General"])
def health():
    return {"status": "healthy", "application": "MediQueue"}


@app.get("/doctors", tags=["Doctors"])
def list_doctors():
    return [{"doctor_id": key, "department": value} for key, value in DOCTORS.items()]


@app.post("/patients", status_code=201, tags=["Patients"])
def create_patient(patient: PatientCreate):
    try:
        return register_patient(patient.name, patient.age, patient.doctor_id)
    except ValueError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc


@app.get("/queue/{doctor_id}", tags=["Queue"])
def doctor_queue(doctor_id: int):
    try:
        return {"doctor_id": doctor_id, "department": DOCTORS[doctor_id],
                "queue": get_doctor_queue(doctor_id)}
    except ValueError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc


@app.get("/token/{token_id}", tags=["Patients"])
def token_status(token_id: str):
    try:
        return get_patient(token_id)
    except KeyError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc


@app.put("/queue/next/{doctor_id}", tags=["Queue"])
def call_next(doctor_id: int):
    try:
        patient = call_next_patient(doctor_id)
    except ValueError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc

    if patient is None:
        return {"message": "No patients waiting"}
    return {"message": "Next patient called", "patient": patient}
