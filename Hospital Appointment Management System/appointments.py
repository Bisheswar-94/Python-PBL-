"""Appointment scheduling and cancellation logic."""

from datetime import date, time


class AppointmentBook:
    def __init__(self):
        self.appointments = {}

    def book(self, patient_id, doctor_id, appointment_date, appointment_time):
        date.fromisoformat(appointment_date)
        time.fromisoformat(appointment_time)
        for existing in self.appointments.values():
            if (
                existing["doctor_id"] == doctor_id
                and existing["date"] == appointment_date
                and existing["time"] == appointment_time
            ):
                raise ValueError("That doctor already has an appointment at that date and time.")
        appointment_id = max(self.appointments, default=0) + 1
        appointment = {
            "id": appointment_id,
            "patient_id": patient_id,
            "doctor_id": doctor_id,
            "date": appointment_date,
            "time": appointment_time,
        }
        self.appointments[appointment_id] = appointment
        return appointment

    def list_all(self):
        return list(self.appointments.values())

    def cancel(self, appointment_id):
        if appointment_id not in self.appointments:
            raise KeyError("Appointment ID was not found.")
        del self.appointments[appointment_id]
