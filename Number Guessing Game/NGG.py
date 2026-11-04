"""Number Guessing Game

Concepts: random numbers and conditional statements.
"""

import random


def play_game():
    secret_number = random.randint(1, 100)
    attempts = 0

    print("\nI picked a number from 1 to 100. Can you guess it?")

    while True:
        try:
            guess_text = input("Enter your guess: ").strip()
        except EOFError:
            print("\nNo input received. Run this game in a terminal so you can enter guesses.")
            return

        if not guess_text.isdigit():
            print("Please enter a whole number.")
            continue

        guess = int(guess_text)
        attempts += 1

        if guess < 1 or guess > 100:
            print("Your guess must be between 1 and 100.")
        elif guess < secret_number:
            print("Too low! Try again.")
        elif guess > secret_number:
            print("Too high! Try again.")
        else:
            print(f"Correct! You guessed the number in {attempts} attempts.")
            break


def main():
    print("=== Number Guessing Game ===")

    while True:
        play_game()
        try:
            play_again = input("Would you like to play again? (y/n): ").strip().lower()
        except EOFError:
            print("\nNo input received. Run this game in a terminal to play again.")
            break

        if play_again != "y":
            print("Thanks for playing!")
            break


if __name__ == "__main__":
    main()
