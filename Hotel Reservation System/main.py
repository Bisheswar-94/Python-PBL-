"""Command-line hotel reservation system with JSON file storage."""

import json
from dataclasses import asdict, dataclass
from datetime import date
from pathlib import Path


DATA_FILE = Path(__file__).with_name("hotel_data.json")


@dataclass
class Room:
    room_number: int
    room_type: str
    price_per_night: float


@dataclass
class Reservation:
    reservation_id: int
    guest_name: str
    room_number: int
    check_in: str
    check_out: str


class Hotel:
    """Keeps room and reservation records and persists them to a JSON file."""

    def __init__(self, data_file=DATA_FILE):
        self.data_file = data_file
        self.rooms = {}
        self.reservations = {}
        self._load()

    def _load(self):
        if not self.data_file.exists():
            self.rooms = {
                101: Room(101, "Single", 75.0),
                102: Room(102, "Double", 110.0),
                201: Room(201, "Suite", 180.0),
            }
            self._save()
            return
        try:
            data = json.loads(self.data_file.read_text(encoding="utf-8"))
            self.rooms = {
                int(item["room_number"]): Room(**item)
                for item in data.get("rooms", [])
            }
            self.reservations = {
                int(item["reservation_id"]): Reservation(**item)
                for item in data.get("reservations", [])
            }
        except (OSError, json.JSONDecodeError, KeyError, TypeError, ValueError) as error:
            print(f"Could not read hotel data: {error}")
            print("Starting with the default rooms and no reservations.")
            self.rooms = {
                101: Room(101, "Single", 75.0),
                102: Room(102, "Double", 110.0),
                201: Room(201, "Suite", 180.0),
            }
            self.reservations = {}

    def _save(self):
        data = {
            "rooms": [asdict(room) for room in self.rooms.values()],
            "reservations": [asdict(item) for item in self.reservations.values()],
        }
        self.data_file.write_text(json.dumps(data, indent=2), encoding="utf-8")

    def available_rooms(self, check_in, check_out):
        occupied = set()
        for reservation in self.reservations.values():
            overlaps = check_in < reservation.check_out and check_out > reservation.check_in
            if overlaps:
                occupied.add(reservation.room_number)
        return [room for number, room in self.rooms.items() if number not in occupied]

    def book_room(self, guest_name, room_number, check_in, check_out):
        if room_number not in {room.room_number for room in self.available_rooms(check_in, check_out)}:
            raise ValueError("That room is not available for the selected dates.")
        reservation_id = max(self.reservations, default=0) + 1
        reservation = Reservation(reservation_id, guest_name, room_number, check_in, check_out)
        self.reservations[reservation_id] = reservation
        self._save()
        return reservation

    def cancel_reservation(self, reservation_id):
        if reservation_id not in self.reservations:
            raise KeyError("Reservation ID was not found.")
        del self.reservations[reservation_id]
        self._save()


def read_date(prompt):
    while True:
        value = input(prompt).strip()
        try:
            parsed = date.fromisoformat(value)
            return parsed.isoformat()
        except ValueError:
            print("Enter a valid date in YYYY-MM-DD format.")


def get_stay_dates():
    while True:
        check_in = read_date("Check-in date (YYYY-MM-DD): ")
        check_out = read_date("Check-out date (YYYY-MM-DD): ")
        if check_out > check_in:
            return check_in, check_out
        print("Check-out must be after check-in. Please enter the dates again.")


def show_rooms(rooms):
    if not rooms:
        print("No rooms are available for those dates.")
        return
    print("\nAvailable rooms")
    for room in rooms:
        print(f"Room {room.room_number}: {room.room_type} — ${room.price_per_night:.2f} per night")


def view_availability(hotel):
    check_in, check_out = get_stay_dates()
    show_rooms(hotel.available_rooms(check_in, check_out))


def make_reservation(hotel):
    check_in, check_out = get_stay_dates()
    available = hotel.available_rooms(check_in, check_out)
    show_rooms(available)
    if not available:
        return
    valid_numbers = {room.room_number for room in available}
    while True:
        try:
            room_number = int(input("Room number to book: ").strip())
        except ValueError:
            print("Enter a numeric room number.")
            continue
        if room_number in valid_numbers:
            break
        print("Choose a room from the available list.")
    guest_name = input("Guest name: ").strip()
    while not guest_name:
        guest_name = input("Guest name cannot be blank. Enter guest name: ").strip()
    reservation = hotel.book_room(guest_name, room_number, check_in, check_out)
    print(f"Reservation confirmed. Your reservation ID is {reservation.reservation_id}.")


def list_reservations(hotel):
    if not hotel.reservations:
        print("There are no reservations.")
        return
    print("\nReservations")
    for reservation in hotel.reservations.values():
        room = hotel.rooms.get(reservation.room_number)
        room_type = room.room_type if room else "Unknown room"
        print(
            f"ID {reservation.reservation_id}: {reservation.guest_name} | "
            f"Room {reservation.room_number} ({room_type}) | "
            f"{reservation.check_in} to {reservation.check_out}"
        )


def cancel_reservation(hotel):
    list_reservations(hotel)
    if not hotel.reservations:
        return
    try:
        reservation_id = int(input("Reservation ID to cancel: ").strip())
        hotel.cancel_reservation(reservation_id)
        print("Reservation cancelled.")
    except ValueError:
        print("Enter a numeric reservation ID.")
    except KeyError as error:
        print(error.args[0])


def main():
    hotel = Hotel()
    actions = {
        "1": lambda: view_availability(hotel),
        "2": lambda: make_reservation(hotel),
        "3": lambda: list_reservations(hotel),
        "4": lambda: cancel_reservation(hotel),
    }
    print("=== Hotel Reservation System ===")
    while True:
        print("\n1. Check room availability\n2. Make a reservation")
        print("3. View reservations\n4. Cancel a reservation\n0. Exit")
        choice = input("Choose an option: ").strip()
        if choice == "0":
            print("Goodbye!")
            break
        action = actions.get(choice)
        if action:
            try:
                action()
            except OSError as error:
                print(f"Could not save hotel data: {error}")
        else:
            print("Please choose one of the listed options.")


if __name__ == "__main__":
    main()
