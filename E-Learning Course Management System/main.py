"""A small command-line e-learning course management system."""

import json
from dataclasses import asdict, dataclass, field
from pathlib import Path


DATA_FILE = Path(__file__).with_name("learning_data.json")


@dataclass
class Course:
    course_id: int
    title: str
    instructor: str
    description: str
    lessons: list[str] = field(default_factory=list)


@dataclass
class Learner:
    learner_id: int
    name: str
    email: str
    enrollments: dict[str, list[int]] = field(default_factory=dict)


class LearningPlatform:
    """Owns courses and learners, and saves/loads them as JSON."""

    def __init__(self, data_file: Path = DATA_FILE):
        self.data_file = data_file
        self.courses: dict[int, Course] = {}
        self.learners: dict[int, Learner] = {}
        self._load()

    def _load(self):
        if not self.data_file.exists():
            return
        try:
            data = json.loads(self.data_file.read_text(encoding="utf-8"))
            self.courses = {
                int(item["course_id"]): Course(**item)
                for item in data.get("courses", [])
            }
            self.learners = {
                int(item["learner_id"]): Learner(**item)
                for item in data.get("learners", [])
            }
        except (OSError, json.JSONDecodeError, KeyError, TypeError, ValueError) as error:
            print(f"Could not load saved data: {error}")
            print("Starting with empty course and learner lists.")
            self.courses = {}
            self.learners = {}

    def save(self):
        data = {
            "courses": [asdict(course) for course in self.courses.values()],
            "learners": [asdict(learner) for learner in self.learners.values()],
        }
        self.data_file.write_text(json.dumps(data, indent=2), encoding="utf-8")

    @staticmethod
    def _next_id(records):
        return max(records, default=0) + 1

    def add_course(self, title, instructor, description, lessons):
        course = Course(self._next_id(self.courses), title, instructor, description, lessons)
        self.courses[course.course_id] = course
        self.save()
        return course

    def add_learner(self, name, email):
        learner = Learner(self._next_id(self.learners), name, email)
        self.learners[learner.learner_id] = learner
        self.save()
        return learner

    def enroll(self, learner_id, course_id):
        learner = self.learners[learner_id]
        course_key = str(course_id)
        if course_key not in learner.enrollments:
            learner.enrollments[course_key] = []
            self.save()

    def mark_lesson_complete(self, learner_id, course_id, lesson_number):
        learner = self.learners[learner_id]
        completed = learner.enrollments[course_id]
        if lesson_number not in completed:
            completed.append(lesson_number)
            completed.sort()
            self.save()


def prompt_nonempty(label):
    while True:
        value = input(label).strip()
        if value:
            return value
        print("Please enter a value.")


def prompt_id(label, records):
    while True:
        try:
            record_id = int(input(label).strip())
        except ValueError:
            print("Enter a numeric ID.")
            continue
        if record_id in records:
            return record_id
        print("That ID was not found.")


def list_courses(platform):
    if not platform.courses:
        print("No courses are available yet.")
        return
    print("\nCourses")
    for course in platform.courses.values():
        print(f"\n[{course.course_id}] {course.title} — {course.instructor}")
        print(course.description)
        if course.lessons:
            for index, lesson in enumerate(course.lessons, start=1):
                print(f"  {index}. {lesson}")
        else:
            print("  No lessons have been added.")


def list_learners(platform):
    if not platform.learners:
        print("No learners are registered yet.")
        return
    print("\nLearners")
    for learner in platform.learners.values():
        print(f"[{learner.learner_id}] {learner.name} — {learner.email}")


def add_course_menu(platform):
    print("\nAdd a course")
    title = prompt_nonempty("Course title: ")
    instructor = prompt_nonempty("Instructor: ")
    description = prompt_nonempty("Description: ")
    print("Enter lesson titles one at a time. Leave blank when finished.")
    lessons = []
    while True:
        lesson = input(f"Lesson {len(lessons) + 1}: ").strip()
        if not lesson:
            break
        lessons.append(lesson)
    course = platform.add_course(title, instructor, description, lessons)
    print(f"Course created with ID {course.course_id}.")


def register_learner_menu(platform):
    print("\nRegister a learner")
    name = prompt_nonempty("Name: ")
    email = prompt_nonempty("Email: ")
    learner = platform.add_learner(name, email)
    print(f"Learner registered with ID {learner.learner_id}.")


def enroll_menu(platform):
    if not platform.learners or not platform.courses:
        print("Register a learner and add a course before enrolling.")
        return
    list_learners(platform)
    learner_id = prompt_id("Learner ID: ", platform.learners)
    list_courses(platform)
    course_id = prompt_id("Course ID: ", platform.courses)
    platform.enroll(learner_id, course_id)
    print("Learner enrolled (or was already enrolled) in the course.")


def learner_progress_menu(platform):
    if not platform.learners:
        print("No learners are registered yet.")
        return
    list_learners(platform)
    learner_id = prompt_id("Learner ID: ", platform.learners)
    learner = platform.learners[learner_id]
    if not learner.enrollments:
        print("This learner is not enrolled in any courses.")
        return
    print(f"\nProgress for {learner.name}")
    for course_id, completed in learner.enrollments.items():
        course = platform.courses.get(int(course_id))
        if course is None:
            continue
        total = len(course.lessons)
        percentage = round(100 * len(completed) / total) if total else 0
        print(f"[{course.course_id}] {course.title}: {len(completed)}/{total} lessons ({percentage}%)")
    answer = input("Mark a lesson complete? (y/n): ").strip().lower()
    if answer != "y":
        return
    enrolled = {
        int(course_id): platform.courses[int(course_id)]
        for course_id in learner.enrollments
        if int(course_id) in platform.courses
    }
    if not enrolled:
        print("No enrolled courses are available.")
        return
    course_id = prompt_id("Course ID: ", enrolled)
    course = enrolled[course_id]
    if not course.lessons:
        print("This course has no lessons yet.")
        return
    for index, lesson in enumerate(course.lessons, start=1):
        marker = "✓" if index in learner.enrollments[str(course_id)] else " "
        print(f"[{marker}] {index}. {lesson}")
    while True:
        try:
            lesson_number = int(input("Lesson number completed: ").strip())
        except ValueError:
            print("Enter a numeric lesson number.")
            continue
        if 1 <= lesson_number <= len(course.lessons):
            platform.mark_lesson_complete(learner_id, str(course_id), lesson_number)
            print("Progress saved.")
            return
        print(f"Choose a lesson from 1 to {len(course.lessons)}.")


def main():
    platform = LearningPlatform()
    actions = {
        "1": lambda: list_courses(platform),
        "2": lambda: add_course_menu(platform),
        "3": lambda: list_learners(platform),
        "4": lambda: register_learner_menu(platform),
        "5": lambda: enroll_menu(platform),
        "6": lambda: learner_progress_menu(platform),
    }
    print("=== E-Learning Course Management System ===")
    while True:
        print("\n1. View courses\n2. Add a course\n3. View learners")
        print("4. Register a learner\n5. Enroll learner in a course")
        print("6. View/update learner progress\n0. Exit")
        choice = input("Choose an option: ").strip()
        if choice == "0":
            print("Goodbye!")
            break
        action = actions.get(choice)
        if action:
            try:
                action()
            except (OSError, json.JSONDecodeError) as error:
                print(f"Could not save the change: {error}")
        else:
            print("Please choose one of the listed options.")


if __name__ == "__main__":
    main()
