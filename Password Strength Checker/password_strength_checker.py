"""A simple password strength checker using string manipulation."""

import string


def check_password_strength(password: str) -> tuple[str, list[str]]:
    """Return a strength rating and suggestions for the supplied password."""
    suggestions: list[str] = []
    score = 0

    if len(password) >= 8:
        score += 1
    else:
        suggestions.append("Use at least 8 characters.")

    if any(character.isupper() for character in password):
        score += 1
    else:
        suggestions.append("Add at least one uppercase letter.")

    if any(character.islower() for character in password):
        score += 1
    else:
        suggestions.append("Add at least one lowercase letter.")

    if any(character.isdigit() for character in password):
        score += 1
    else:
        suggestions.append("Add at least one number.")

    if any(character in string.punctuation for character in password):
        score += 1
    else:
        suggestions.append("Add at least one special character.")

    if score <= 2:
        strength = "Weak"
    elif score <= 4:
        strength = "Moderate"
    else:
        strength = "Strong"

    return strength, suggestions


def main() -> None:
    """Read a password and display its strength."""
    password = input("Enter a password: ")
    strength, suggestions = check_password_strength(password)

    print(f"\nPassword strength: {strength}")
    if suggestions:
        print("Suggestions:")
        for suggestion in suggestions:
            print(f"- {suggestion}")
    else:
        print("Good job! Your password meets all the basic requirements.")


if __name__ == "__main__":
    main()
