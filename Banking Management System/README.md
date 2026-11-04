# Banking Management System

A local Python web app demonstrating project packages and reusable functions.

## Run

1. Install Python 3 (no third-party packages needed).
2. Open a terminal in this folder.
3. Run `python web_app.py`.
4. Open http://127.0.0.1:8001.

Data is saved locally in `bank_data.json`, created on first use. Educational demo only; do not use real customer information or real credentials.

## Packages and functions

- `banking/` is a Python package, identified by `__init__.py`.
- `banking.accounts` contains `create_account`, `list_accounts`, and `close_account`.
- `banking.transactions` contains `deposit`, `withdraw`, `transfer`, and `history`.
- `banking.storage` centralizes JSON read/write functions.
- `web_app.py` imports package functions and exposes them through an HTTP API.

## Layout

```text
Banking Management System/
├── banking/
│   ├── __init__.py
│   ├── accounts.py
│   ├── storage.py
│   └── transactions.py
├── static/
│   ├── app.js
│   ├── index.html
│   └── style.css
├── web_app.py
└── README.md
```
