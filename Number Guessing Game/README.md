# Number Guessing Game

A simple command-line game written in Python. The computer chooses a random number from 1 to 100, and you try to guess it. The game gives a hint after each valid guess and tells you how many attempts you needed.

## Requirements

- Python 3
- A terminal or command prompt for entering guesses

No external packages are required; the game uses Python's built-in `random` module.

## Run the game

Open a terminal in this folder and run:

```bash
python NGG.py
```

On some systems, use `python3 NGG.py` instead.

## How to play

1. Enter a whole number between 1 and 100.
2. Follow the `Too low!` or `Too high!` hint and guess again.
3. When you find the number, the game reports your number of attempts.
4. Enter `y` when asked to start another round. Any other response ends the game.

Inputs that are not whole numbers are rejected. Guesses outside the 1–100 range receive a range reminder.

## Project file

- `NGG.py` — game logic and command-line prompts.
