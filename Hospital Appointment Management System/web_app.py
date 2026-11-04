"""Dependency-free web application for hospital appointment management."""

import json
from datetime import date, time
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import urlparse


ROOT = Path(__file__).parent
DATA_FILE = ROOT / "hospital_data.json"
HOST = "127.0.0.1"
PORT = 8000


class HospitalService:
    """Application operations and JSON persistence for the web interface."""

    def __init__(self, data_file=DATA_FILE):
        self.data_file = data_file
        self.patients = []
        self.doctors = []
        self.appointments = []
        self._load()

    def _load(self):
        if not self.data_file.exists():
            return
        try:
            data = json.loads(self.data_file.read_text(encoding="utf-8"))
            self.patients = data.get("patients", [])
            self.doctors = data.get("doctors", [])
            self.appointments = data.get("appointments", [])
        except (OSError, json.JSONDecodeError, TypeError) as error:
            print(f"Could not load saved hospital data: {error}")

    def save(self):
        data = {
            "patients": self.patients,
            "doctors": self.doctors,
            "appointments": self.appointments,
        }
        self.data_file.write_text(json.dumps(data, indent=2), encoding="utf-8")

    @staticmethod
    def next_id(records):
        return max((record["id"] for record in records), default=0) + 1

    @staticmethod
    def required_text(payload, field):
        value = str(payload.get(field, "")).strip()
        if not value:
            raise ValueError(f"{field.replace('_', ' ').capitalize()} is required.")
        return value

    def create_patient(self, payload):
        patient = {
            "id": self.next_id(self.patients),
            "name": self.required_text(payload, "name"),
            "phone": self.required_text(payload, "phone"),
            "email": str(payload.get("email", "")).strip(),
        }
        self.patients.append(patient)
        self.save()
        return patient

    def update_patient(self, patient_id, payload):
        patient = self.find(self.patients, patient_id)
        patient.update({
            "name": self.required_text(payload, "name"),
            "phone": self.required_text(payload, "phone"),
            "email": str(payload.get("email", "")).strip(),
        })
        self.save()
        return patient

    def delete_patient(self, patient_id):
        self.find(self.patients, patient_id)
        self.patients = [item for item in self.patients if item["id"] != patient_id]
        self.appointments = [item for item in self.appointments if item["patient_id"] != patient_id]
        self.save()

    def create_doctor(self, payload):
        doctor = {
            "id": self.next_id(self.doctors),
            "name": self.required_text(payload, "name"),
            "specialty": self.required_text(payload, "specialty"),
            "phone": str(payload.get("phone", "")).strip(),
        }
        self.doctors.append(doctor)
        self.save()
        return doctor

    def update_doctor(self, doctor_id, payload):
        doctor = self.find(self.doctors, doctor_id)
        doctor.update({
            "name": self.required_text(payload, "name"),
            "specialty": self.required_text(payload, "specialty"),
            "phone": str(payload.get("phone", "")).strip(),
        })
        self.save()
        return doctor

    def delete_doctor(self, doctor_id):
        self.find(self.doctors, doctor_id)
        self.doctors = [item for item in self.doctors if item["id"] != doctor_id]
        self.appointments = [item for item in self.appointments if item["doctor_id"] != doctor_id]
        self.save()

    def create_appointment(self, payload):
        patient_id = int(payload.get("patient_id", 0))
        doctor_id = int(payload.get("doctor_id", 0))
        self.find(self.patients, patient_id)
        self.find(self.doctors, doctor_id)
        appointment_date = self.required_text(payload, "date")
        appointment_time = self.required_text(payload, "time")
        date.fromisoformat(appointment_date)
        time.fromisoformat(appointment_time)
        for existing in self.appointments:
            if (existing["doctor_id"] == doctor_id
                    and existing["date"] == appointment_date
                    and existing["time"] == appointment_time):
                raise ValueError("This doctor already has an appointment at that date and time.")
        appointment = {
            "id": self.next_id(self.appointments),
            "patient_id": patient_id,
            "doctor_id": doctor_id,
            "date": appointment_date,
            "time": appointment_time,
            "reason": str(payload.get("reason", "")).strip(),
        }
        self.appointments.append(appointment)
        self.save()
        return appointment

    def update_appointment(self, appointment_id, payload):
        old = self.find(self.appointments, appointment_id)
        replacement = dict(payload)
        replacement["patient_id"] = int(payload.get("patient_id", old["patient_id"]))
        replacement["doctor_id"] = int(payload.get("doctor_id", old["doctor_id"]))
        replacement["date"] = self.required_text(payload, "date")
        replacement["time"] = self.required_text(payload, "time")
        self.find(self.patients, replacement["patient_id"])
        self.find(self.doctors, replacement["doctor_id"])
        date.fromisoformat(replacement["date"])
        time.fromisoformat(replacement["time"])
        for existing in self.appointments:
            if existing["id"] != appointment_id and (
                existing["doctor_id"] == replacement["doctor_id"]
                and existing["date"] == replacement["date"]
                and existing["time"] == replacement["time"]
            ):
                raise ValueError("This doctor already has an appointment at that date and time.")
        old.update({key: replacement[key] for key in ("patient_id", "doctor_id", "date", "time")})
        old["reason"] = str(payload.get("reason", "")).strip()
        self.save()
        return old

    def delete_appointment(self, appointment_id):
        self.find(self.appointments, appointment_id)
        self.appointments = [item for item in self.appointments if item["id"] != appointment_id]
        self.save()

    @staticmethod
    def find(records, record_id):
        for record in records:
            if record["id"] == record_id:
                return record
        raise KeyError("Record not found.")

    def overview(self):
        patients = {item["id"]: item for item in self.patients}
        doctors = {item["id"]: item for item in self.doctors}
        appointments = []
        for appointment in self.appointments:
            patient = patients.get(appointment["patient_id"])
            doctor = doctors.get(appointment["doctor_id"])
            if patient and doctor:
                appointments.append({
                    **appointment,
                    "patient_name": patient["name"],
                    "doctor_name": doctor["name"],
                    "doctor_specialty": doctor["specialty"],
                })
        appointments.sort(key=lambda item: (item["date"], item["time"]))
        return {"patients": self.patients, "doctors": self.doctors, "appointments": appointments}


service = HospitalService()


class RequestHandler(BaseHTTPRequestHandler):
    def send_json(self, status, payload):
        body = json.dumps(payload).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def read_json(self):
        length = int(self.headers.get("Content-Length", "0"))
        if length > 1_000_000:
            raise ValueError("Request is too large.")
        return json.loads(self.rfile.read(length) or b"{}")

    def do_GET(self):
        path = urlparse(self.path).path
        if path == "/":
            body = (ROOT / "static" / "index.html").read_bytes()
            self.send_response(200)
            self.send_header("Content-Type", "text/html; charset=utf-8")
            self.send_header("Content-Length", str(len(body)))
            self.end_headers()
            self.wfile.write(body)
        elif path == "/style.css" or path == "/app.js":
            asset = ROOT / "static" / path.lstrip("/")
            body = asset.read_bytes()
            content_type = "text/css; charset=utf-8" if path.endswith(".css") else "text/javascript; charset=utf-8"
            self.send_response(200)
            self.send_header("Content-Type", content_type)
            self.send_header("Content-Length", str(len(body)))
            self.end_headers()
            self.wfile.write(body)
        elif path == "/api/data":
            self.send_json(200, service.overview())
        else:
            self.send_json(404, {"error": "Not found."})

    def do_POST(self):
        self.mutate("POST")

    def do_PUT(self):
        self.mutate("PUT")

    def do_DELETE(self):
        self.mutate("DELETE")

    def mutate(self, method):
        path = urlparse(self.path).path.strip("/").split("/")
        try:
            payload = self.read_json() if method in ("POST", "PUT") else {}
            if len(path) == 2 and path[0] == "api" and method == "POST":
                collection = path[1]
                create = {
                    "patients": service.create_patient,
                    "doctors": service.create_doctor,
                    "appointments": service.create_appointment,
                }.get(collection)
                if not create:
                    raise KeyError("Unknown collection.")
                record = create(payload)
            elif len(path) == 3 and path[0] == "api" and path[1] in ("patients", "doctors", "appointments"):
                collection, record_id = path[1], int(path[2])
                if method == "DELETE":
                    delete = {
                        "patients": service.delete_patient,
                        "doctors": service.delete_doctor,
                        "appointments": service.delete_appointment,
                    }[collection]
                    delete(record_id)
                    record = {"id": record_id, "deleted": True}
                elif method == "PUT":
                    update = {
                        "patients": service.update_patient,
                        "doctors": service.update_doctor,
                        "appointments": service.update_appointment,
                    }[collection]
                    record = update(record_id, payload)
                else:
                    raise KeyError("Unsupported operation.")
            else:
                raise KeyError("Not found.")
            self.send_json(200, {"record": record, "data": service.overview()})
        except (ValueError, TypeError, json.JSONDecodeError) as error:
            self.send_json(400, {"error": str(error) or "Invalid request."})
        except KeyError as error:
            self.send_json(404, {"error": error.args[0] if error.args else "Record not found."})
        except OSError as error:
            self.send_json(500, {"error": f"Could not save data: {error}"})

    def log_message(self, format_string, *args):
        print(f"[{self.log_date_time_string()}] {format_string % args}")


def main():
    server = ThreadingHTTPServer((HOST, PORT), RequestHandler)
    print(f"Hospital Appointment Management is running at http://{HOST}:{PORT}")
    print("Press Ctrl+C to stop the server.")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nStopping server...")
    finally:
        server.server_close()


if __name__ == "__main__":
    main()
