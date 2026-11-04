"""Main menu for the modular Hospital Appointment Management System."""

from appointments import AppointmentBook
from doctors import DoctorDirectory
from patients import PatientRegistry


def read_id(prompt):
    while True:
        try:
            return int(input(prompt).strip())
        except ValueError:
            print("Enter a numeric ID.")


def show_patients(registry):
    patients = registry.list_all()
    if not patients:
        print("No patients registered yet.")
        return
    print("\nPatients")
    for patient in patients:
        print(f"[{patient['id']}] {patient['name']} — {patient['phone']}")


def show_doctors(directory):
    doctors = directory.list_all()
    if not doctors:
        print("No doctors registered yet.")
        return
    print("\nDoctors")
    for doctor in doctors:
        print(f"[{doctor['id']}] Dr. {doctor['name']} — {doctor['specialty']}")


def add_patient(registry):
    name = input("Patient name: ").strip()
    phone = input("Phone number: ").strip()
    if not name or not phone:
        print("Name and phone number are required.")
        return
    patient = registry.add(name, phone)
    print(f"Patient added with ID {patient['id']}.")


def add_doctor(directory):
    name = input("Doctor name: ").strip()
    specialty = input("Specialty: ").strip()
    if not name or not specialty:
        print("Name and specialty are required.")
        return
    doctor = directory.add(name, specialty)
    print(f"Doctor added with ID {doctor['id']}.")


def book_appointment(registry, directory, book):
    if not registry.list_all() or not directory.list_all():
        print("Add at least one patient and one doctor before booking.")
        return
    show_patients(registry)
    patient_id = read_id("Patient ID: ")
    if not registry.get(patient_id):
        print("Patient ID was not found.")
        return
    show_doctors(directory)
    doctor_id = read_id("Doctor ID: ")
    if not directory.get(doctor_id):
        print("Doctor ID was not found.")
        return
    appointment_date = input("Date (YYYY-MM-DD): ").strip()
    appointment_time = input("Time (HH:MM, 24-hour): ").strip()
    try:
        appointment = book.book(patient_id, doctor_id, appointment_date, appointment_time)
        print(f"Appointment booked with ID {appointment['id']}.")
    except ValueError as error:
        print(f"Could not book appointment: {error}")


def show_appointments(registry, directory, book):
    appointments = book.list_all()
    if not appointments:
        print("No appointments scheduled.")
        return
    print("\nAppointments")
    for appointment in appointments:
        patient = registry.get(appointment["patient_id"])
        doctor = directory.get(appointment["doctor_id"])
        print(
            f"[{appointment['id']}] {appointment['date']} {appointment['time']} | "
            f"Patient: {patient['name']} | Doctor: Dr. {doctor['name']} ({doctor['specialty']})"
        )


def cancel_appointment(book):
    if not book.list_all():
        print("No appointments to cancel.")
        return
    appointment_id = read_id("Appointment ID to cancel: ")
    try:
        book.cancel(appointment_id)
        print("Appointment cancelled.")
    except KeyError as error:
        print(error.args[0])


def main():
    patients = PatientRegistry()
    doctors = DoctorDirectory()
    appointments = AppointmentBook()
    while True:
        print("\n=== Hospital Appointment Management System ===")
        print("1. Add patient\n2. List patients\n3. Add doctor\n4. List doctors")
        print("5. Book appointment\n6. List appointments\n7. Cancel appointment\n0. Exit")
        choice = input("Choose an option: ").strip()
        actions = {
            "1": lambda: add_patient(patients),
            "2": lambda: show_patients(patients),
            "3": lambda: add_doctor(doctors),
            "4": lambda: show_doctors(doctors),
            "5": lambda: book_appointment(patients, doctors, appointments),
            "6": lambda: show_appointments(patients, doctors, appointments),
            "7": lambda: cancel_appointment(appointments),
        }
        if choice == "0":
            print("Goodbye!")
            break
        action = actions.get(choice)
        if action:
            action()
        else:
            print("Please choose one of the listed options.")


if __name__ == "__main__":
    main()
