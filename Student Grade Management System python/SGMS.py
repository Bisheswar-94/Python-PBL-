"""Student Grade Management System.

This beginner-friendly console project demonstrates variables, conditions,
loops, functions, lists, and dictionaries without external dependencies.
"""

from __future__ import annotations

from typing import Dict, List


SUBJECTS = ("English", "Mathematics", "Science", "Computer")
PASS_MARK = 40


def calculate_grade(average: float) -> str:
    """Return a letter grade for an average mark."""
    if average >= 90:
        return "A+"
    if average >= 80:
        return "A"
    if average >= 70:
        return "B"
    if average >= 60:
        return "C"
    if average >= 50:
        return "D"
    if average >= PASS_MARK:
        return "E"
    return "F"


def calculate_result(marks: Dict[str, int]) -> tuple[int, float, str, str]:
    """Calculate total, average, grade, and pass/fail result."""
    total = sum(marks.values())
    average = total / len(marks)
    grade = calculate_grade(average)
    passed = all(mark >= PASS_MARK for mark in marks.values())
    result = "Pass" if passed else "Fail"
    return total, average, grade, result


def read_non_empty(prompt: str) -> str:
    """Read text until the user enters a non-empty value."""
    while True:
        value = input(prompt).strip()
        if value:
            return value
        print("Input cannot be empty.")


def read_integer(prompt: str, minimum: int, maximum: int) -> int:
    """Read an integer within an inclusive range."""
    while True:
        value = input(prompt).strip()
        try:
            number = int(value)
        except ValueError:
            print("Please enter a whole number.")
            continue
        if minimum <= number <= maximum:
            return number
        print(f"Enter a number from {minimum} to {maximum}.")


def read_marks() -> Dict[str, int]:
    """Read marks for every subject."""
    marks: Dict[str, int] = {}
    for subject in SUBJECTS:
        marks[subject] = read_integer(f"{subject} mark (0-100): ", 0, 100)
    return marks


def add_student(students: List[dict]) -> None:
    """Add one student after collecting their details."""
    print("\n--- Add Student ---")
    student_id = read_non_empty("Student ID: ")
    if any(student["id"].lower() == student_id.lower() for student in students):
        print("A student with that ID already exists.")
        return

    name = read_non_empty("Student name: ")
    marks = read_marks()
    students.append({"id": student_id, "name": name, "marks": marks})
    print("Student added successfully.")


def print_student(student: dict) -> None:
    """Display one student's marks and calculated result."""
    total, average, grade, result = calculate_result(student["marks"])
    print(f"\nID: {student['id']} | Name: {student['name']}")
    for subject, mark in student["marks"].items():
        print(f"  {subject}: {mark}")
    print(f"  Total: {total}/{len(SUBJECTS) * 100}")
    print(f"  Average: {average:.2f}")
    print(f"  Grade: {grade} | Result: {result}")


def find_student(students: List[dict], student_id: str) -> dict | None:
    """Find a student by ID, ignoring letter case."""
    for student in students:
        if student["id"].lower() == student_id.lower():
            return student
    return None


def view_students(students: List[dict]) -> None:
    """Display all students."""
    print("\n--- All Students ---")
    if not students:
        print("No student records found.")
        return
    for student in students:
        print_student(student)


def search_student(students: List[dict]) -> None:
    """Search for and display one student."""
    print("\n--- Search Student ---")
    student_id = read_non_empty("Enter student ID: ")
    student = find_student(students, student_id)
    if student is None:
        print("Student not found.")
    else:
        print_student(student)


def update_student(students: List[dict]) -> None:
    """Replace the marks for an existing student."""
    print("\n--- Update Student Marks ---")
    student_id = read_non_empty("Enter student ID: ")
    student = find_student(students, student_id)
    if student is None:
        print("Student not found.")
        return
    print(f"Enter new marks for {student['name']}.")
    student["marks"] = read_marks()
    print("Student marks updated successfully.")


def delete_student(students: List[dict]) -> None:
    """Delete an existing student after confirmation."""
    print("\n--- Delete Student ---")
    student_id = read_non_empty("Enter student ID: ")
    student = find_student(students, student_id)
    if student is None:
        print("Student not found.")
        return
    confirmation = input(f"Delete {student['name']}? (y/n): ").strip().lower()
    if confirmation == "y":
        students.remove(student)
        print("Student deleted successfully.")
    else:
        print("Delete cancelled.")


def show_summary(students: List[dict]) -> None:
    """Display class totals and the highest-performing student."""
    print("\n--- Class Summary ---")
    if not students:
        print("No student records found.")
        return

    averages = []
    passed = 0
    for student in students:
        _, average, _, result = calculate_result(student["marks"])
        averages.append((average, student))
        if result == "Pass":
            passed += 1

    class_average = sum(average for average, _ in averages) / len(averages)
    top_average, top_student = max(averages, key=lambda item: item[0])
    print(f"Total students: {len(students)}")
    print(f"Passed: {passed}")
    print(f"Failed: {len(students) - passed}")
    print(f"Class average: {class_average:.2f}")
    print(f"Top student: {top_student['name']} ({top_average:.2f})")


def show_menu() -> None:
    """Print the main menu."""
    print(
        "\n===== Student Grade Management System =====\n"
        "1. Add student\n"
        "2. View all students\n"
        "3. Search student\n"
        "4. Update student marks\n"
        "5. Delete student\n"
        "6. Show class summary\n"
        "7. Exit"
    )


def main() -> None:
    """Run the menu until the user chooses to exit."""
    students: List[dict] = []
    print("Welcome to the Student Grade Management System!")

    while True:
        show_menu()
        choice = read_integer("Choose an option (1-7): ", 1, 7)
        if choice == 1:
            add_student(students)
        elif choice == 2:
            view_students(students)
        elif choice == 3:
            search_student(students)
        elif choice == 4:
            update_student(students)
        elif choice == 5:
            delete_student(students)
        elif choice == 6:
            show_summary(students)
        else:
            print("Thank you for using the Student Grade Management System.")
            break


if __name__ == "__main__":
    main()