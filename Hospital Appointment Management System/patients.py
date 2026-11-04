"""Patient records for the hospital appointment application."""


class PatientRegistry:
    def __init__(self):
        self.patients = {}

    def add(self, name, phone):
        patient_id = max(self.patients, default=0) + 1
        patient = {"id": patient_id, "name": name, "phone": phone}
        self.patients[patient_id] = patient
        return patient

    def list_all(self):
        return list(self.patients.values())

    def get(self, patient_id):
        return self.patients.get(patient_id)
