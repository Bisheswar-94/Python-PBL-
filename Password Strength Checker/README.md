# Password Strength Checker

A beginner-friendly Python program that checks whether a password is **Weak**,
**Moderate**, or **Strong**.

## Concepts Used

- String manipulation with `len()`
- String character checks with `isupper()`, `islower()`, and `isdigit()`
- The `any()` function
- Functions and return values
- A conditional `if __name__ == "__main__"` block

## Rules

The checker awards one point for each requirement:

1. At least 8 characters
2. One uppercase letter
3. One lowercase letter
4. One number
5. One special character

Scores from 0–2 are **Weak**, 3–4 are **Moderate**, and 5 is **Strong**.

## How to Run

Make sure Python 3 is installed, then run:

```bash
python password_strength_checker.py
```

The program displays suggestions for any missing requirements. Passwords are
checked locally and are not saved or sent anywhere.
