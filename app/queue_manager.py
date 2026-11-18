from collections import defaultdict
from threading import Lock

DOCTORS = {
    1: "Cardiologist",
    2: "Dentist",
    3: "Neurologist",
}

patients = {}
queues = defaultdict(list)
token_counters = defaultdict(int)
queue_lock = Lock()


def register_patient(name: str, age: int, doctor_id: int):
    with queue_lock:
        if doctor_id not in DOCTORS:
            raise ValueError("Doctor not found")

        token_counters[doctor_id] += 1
        token = f"{doctor_id}-{token_counters[doctor_id]:03d}"

        patients[token] = {
            "token": token,
            "name": name,
            "age": age,
            "doctor_id": doctor_id,
            "doctor": DOCTORS[doctor_id],
            "status": "Waiting",
        }
        queues[doctor_id].append(token)
        position = len(queues[doctor_id])

        return {
            "message": "Patient registered successfully",
            "token": token,
            "queue_position": position,
            "estimated_waiting_time_minutes": max(position - 1, 0) * 10,
            "status": "Waiting",
        }


def get_doctor_queue(doctor_id: int):
    if doctor_id not in DOCTORS:
        raise ValueError("Doctor not found")
    with queue_lock:
        return [
            {**patients[token], "queue_position": index}
            for index, token in enumerate(queues[doctor_id], start=1)
        ]


def get_patient(token: str):
    with queue_lock:
        patient = patients.get(token)
        if patient is None:
            raise KeyError("Token not found")
        return dict(patient)


def call_next_patient(doctor_id: int):
    if doctor_id not in DOCTORS:
        raise ValueError("Doctor not found")
    with queue_lock:
        # Remove any stale entries and call the first patient still waiting.
        while queues[doctor_id]:
            token = queues[doctor_id].pop(0)
            if patients[token]["status"] == "Waiting":
                patients[token]["status"] = "In Consultation"
                return dict(patients[token])
        return None
