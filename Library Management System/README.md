# Library Management System

A local Python web app for managing a small book collection. It demonstrates lists and dictionaries in a practical project.

## Run

1. Install Python 3.
2. Open a terminal in this folder.
3. Run `python web_app.py`.
4. Open http://127.0.0.1:8002.

No third-party packages are required. The app saves its data to `library_data.json` in this folder.

## Concepts used

- `books` is a Python list containing one dictionary per book.
- Each book dictionary stores title, author, category, total copies, available copies, and a list of borrower names.
- List methods such as `append`, `remove`, and comprehensions add, remove, and search records.
- Functions in `library/books.py` add books, find records, borrow and return copies, and remove books.
- `library/data.py` loads and saves the list of dictionaries as JSON.

## Structure

```text
Library Management System/
├── library/
│   ├── __init__.py
│   ├── books.py
│   └── data.py
├── static/
│   ├── app.js
│   ├── index.html
│   └── style.css
├── web_app.py
└── README.md
```
