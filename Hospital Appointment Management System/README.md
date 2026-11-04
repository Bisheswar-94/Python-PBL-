# Hospital Appointment Management System

A browser-based hospital appointment manager for registering patients and doctors and managing appointments. It demonstrates **modular programming** by splitting the application into focused Python modules.

## Concept covered: Modular Programming

Modules keep related functionality together and make a program easier to understand and maintain. This project separates responsibilities as follows:

- `web_app.py` — local web server, application operations, and JSON file storage.
- `static/index.html`, `static/style.css`, `static/app.js` — website interface and browser behavior.
- `patients.py`, `doctors.py`, `appointments.py` — focused patient, doctor, and appointment modules used by the command-line version.
- `main.py` — optional command-line version.

From the website, you can add, edit, list, and delete patients and doctors; schedule, edit, and cancel appointments; and view the appointment list. The system prevents scheduling the same doctor for two appointments at the same date and time. Patient, doctor, and appointment records are saved in `hospital_data.json`.

## Requirements

- Python 3
- No external packages are required for a standard-library implementation.

## Run

Start the website from this folder:

```bash
python web_app.py
```

On some systems, use `python3 web_app.py` instead. Then open [http://127.0.0.1:8000](http://127.0.0.1:8000) in your browser. Stop the server with `Ctrl+C`. No packages need to be installed.

## Project files

Appointment dates use `YYYY-MM-DD` and times use 24-hour format. Data is stored locally beside the application. Deleting a patient or doctor also removes their associated appointments.
