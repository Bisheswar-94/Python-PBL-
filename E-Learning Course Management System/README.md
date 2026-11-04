# E-Learning Course Management System

A command-line application for managing courses, learners, enrollments, and lesson progress. It demonstrates **Object-Oriented Programming (OOP)** and **data persistence** using JSON.

## Concepts covered

- **Classes and objects:** `Course` and `Learner` model the main entities; `LearningPlatform` manages them.
- **Data persistence:** Courses, learners, enrollments, and completed lessons are saved in `learning_data.json` and loaded when the program starts.
- **Encapsulation:** Platform operations add courses and learners, enroll learners, and update progress while keeping persistence in one place.

## Features

- Add and view courses with instructor, description, and lesson titles.
- Register and view learners.
- Enroll learners in courses.
- View lesson completion and mark lessons complete.
- Save changes automatically between runs.

## Requirements

- Python 3
- No external packages are required.

## Run

From this folder, run:

```bash
python main.py
```

On some systems, use `python3 main.py` instead. The application creates `learning_data.json` in this folder the first time it saves data.

## Project contents

- `main.py` — command-line interface, domain classes, and JSON persistence.
- `learning_data.json` — created automatically when you add data; stores courses and learners.
