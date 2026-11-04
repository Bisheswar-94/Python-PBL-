# Hotel Reservation System

A command-line application for checking room availability and managing hotel reservations. It demonstrates **Object-Oriented Programming (OOP)** and **file storage** by organizing rooms and reservations into objects and saving reservation information as JSON between runs.

## Concepts covered

- **OOP:** `Room` and `Reservation` model hotel records; `Hotel` handles availability, bookings, cancellations, and storage.
- **File storage:** Room and reservation data is saved to and loaded from `hotel_data.json`.

## Features

- Check room availability for a date range.
- Book an available room for a guest.
- View and cancel reservations by reservation ID.
- Start with three sample rooms when no data file exists.
- Save changes automatically between runs.

## Requirements

- Python 3
- No external packages are required for a standard-library implementation.

## Run

Run the program from this folder:

```bash
python main.py
```

On some systems, use `python3 main.py` instead. Enter reservation dates in `YYYY-MM-DD` format. The application creates `hotel_data.json` in this folder automatically.

## Project files

- `main.py` — command-line interface, hotel classes, and reservation logic.
- `hotel_data.json` — created automatically to store rooms and reservations.
