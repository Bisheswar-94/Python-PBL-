"""Doctor records for the hospital appointment application."""


class DoctorDirectory:
    def __init__(self):
        self.doctors = {}

    def add(self, name, specialty):
        doctor_id = max(self.doctors, default=0) + 1
        doctor = {"id": doctor_id, "name": name, "specialty": specialty}
        self.doctors[doctor_id] = doctor
        return doctor

    def list_all(self):
        return list(self.doctors.values())

    def get(self, doctor_id):
        return self.doctors.get(doctor_id)
