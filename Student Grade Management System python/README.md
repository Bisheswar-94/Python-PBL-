# Student Grade Management System

A beginner-friendly Python console project for storing student marks and
calculating grades. It demonstrates **variables, conditions, loops,
dictionaries, lists, functions, and input validation**.

## Features

- Add a student with marks for English, Mathematics, Science, and Computer
- Calculate total, average, grade, and pass/fail result
- View every student record
- Search for a student by ID
- Update marks
- Delete a student with confirmation
- Display class average, pass count, fail count, and top student
- Validate empty input, duplicate IDs, and marks from 0 to 100
- Uses only Python's standard library

## Grade Rules

| Average | Grade |
| --- | --- |
| 90-100 | A+ |
| 80-89 | A |
| 70-79 | B |
| 60-69 | C |
| 50-59 | D |
| 40-49 | E |
| Below 40 | F |

A student passes only when their mark in **every subject** is at least 40.

## Requirements

- Python 3.10 or newer

## Run the Program

Open PowerShell and run:

```powershell
cd "D:\Python PBL Bisheswar\Student Grade Management System python"
python ".\SGMS.py"
```

If `python` is not recognized, use the full path to your Python executable:

```powershell
& "C:\Path\To\python.exe" ".\SGMS.py"
```

Follow the numbered menu and enter the requested values. The data is held in
memory while the program is running; closing the program clears the records.

## Project Structure

```text
Student Grade Management System python/
├── SGMS.py
└── README.md
```

## Main Programming Concepts

- **Variables:** store student names, IDs, marks, totals, and averages.
- **Conditions:** validate input and select grades using `if`/`elif`/`else`.
- **Loops:** repeat the menu, input validation, subject entry, and student
  searching.
- **Lists and dictionaries:** store multiple student records and subject marks.
- **Functions:** divide the program into small reusable operations.
