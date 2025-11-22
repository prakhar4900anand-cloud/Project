"""
Password Generator Project
--------------------------

Features:
- Interactive menu
- Customizable password policy:
  - Length
  - Uppercase / lowercase / digits / symbols
- Batch generation (multiple passwords at once)
- Basic password strength evaluation
"""

import string
import secrets
from dataclasses import dataclass


@dataclass
class PasswordPolicy:
    length: int = 12
    use_lowercase: bool = True
    use_uppercase: bool = True
    use_digits: bool = True
    use_symbols: bool = True


class PasswordGeneratorError(Exception):
    """Custom exception for password generator errors."""
    pass


def build_character_pool(policy: PasswordPolicy) -> str:
    """Build the pool of characters based on the chosen policy."""
    pool = ""

    if policy.use_lowercase:
        pool += string.ascii_lowercase
    if policy.use_uppercase:
        pool += string.ascii_uppercase
    if policy.use_digits:
        pool += string.digits
    if policy.use_symbols:
        # You can customize which symbols you want to allow
        pool += "!@#$%^&*()-_=+[]{};:,.<>?/"

    if not pool:
        raise PasswordGeneratorError("No character types selected. Please enable at least one type.")

    return pool


def generate_password(policy: PasswordPolicy) -> str:
    """Generate a single password according to the given policy."""
    if policy.length <= 0:
        raise PasswordGeneratorError("Password length must be positive.")

    pool = build_character_pool(policy)

    # Ensure the password meets the criteria by including at least one of each selected type
    password_chars = []

    # Add at least one from each selected category (for better strength)
    if policy.use_lowercase:
        password_chars.append(secrets.choice(string.ascii_lowercase))
    if policy.use_uppercase:
        password_chars.append(secrets.choice(string.ascii_uppercase))
    if policy.use_digits:
        password_chars.append(secrets.choice(string.digits))
    if policy.use_symbols:
        password_chars.append(secrets.choice("!@#$%^&*()-_=+[]{};:,.<>?/"))

    # Fill the remaining length with random chars from the full pool
    while len(password_chars) < policy.length:
        password_chars.append(secrets.choice(pool))

    # Shuffle the characters so the first few are not predictable
    # secrets.choice doesn’t shuffle, so we can use secrets for indices
    for i in range(len(password_chars)):
        j = secrets.randbelow(len(password_chars))
        password_chars[i], password_chars[j] = password_chars[j], password_chars[i]

    return "".join(password_chars)


def evaluate_strength(password: str) -> str:
    """
    Simple heuristic to evaluate password strength.
    This is basic and only for educational purposes.
    """
    length_score = len(password)

    lower = any(c.islower() for c in password)
    upper = any(c.isupper() for c in password)
    digits = any(c.isdigit() for c in password)
    symbols = any(c in "!@#$%^&*()-_=+[]{};:,.<>?/" for c in password)

    variety_score = sum([lower, upper, digits, symbols])

    # Combine scores
    total_score = length_score + (variety_score * 2)

    if total_score < 10:
        return "Weak"
    elif total_score < 18:
        return "Moderate"
    elif total_score < 26:
        return "Strong"
    else:
        return "Very Strong"


def get_yes_no(prompt: str) -> bool:
    """Utility to safely get a yes/no answer from the user."""
    while True:
        ans = input(prompt + " (y/n): ").strip().lower()
        if ans in ("y", "yes"):
            return True
        if ans in ("n", "no"):
            return False
        print("Invalid input. Please type 'y' or 'n'.")


def get_int(prompt: str, min_value: int = None, max_value: int = None) -> int:
    """Utility to safely get an integer from the user."""
    while True:
        value = input(prompt + ": ").strip()
        if not value.isdigit():
            print("Please enter a valid positive integer.")
            continue

        value = int(value)
        if min_value is not None and value < min_value:
            print(f"Please enter a value >= {min_value}.")
            continue
        if max_value is not None and value > max_value:
            print(f"Please enter a value <= {max_value}.")
            continue
        return value


def prompt_for_policy() -> PasswordPolicy:
    """Interactively ask the user for password policy settings."""
    print("\n--- Configure Password Policy ---")

    length = get_int("Enter desired password length", min_value=4)

    use_lowercase = get_yes_no("Include lowercase letters (a-z)?")
    use_uppercase = get_yes_no("Include uppercase letters (A-Z)?")
    use_digits = get_yes_no("Include digits (0-9)?")
    use_symbols = get_yes_no("Include symbols (!,@,#,...) ?")

    policy = PasswordPolicy(
        length=length,
        use_lowercase=use_lowercase,
        use_uppercase=use_uppercase,
        use_digits=use_digits,
        use_symbols=use_symbols,
    )

    # Ensure at least one character type is true
    if not any([policy.use_lowercase, policy.use_uppercase, policy.use_digits, policy.use_symbols]):
        print("You must select at least one character type. Using default policy instead.")
        policy = PasswordPolicy(length=length)

    return policy


def generate_single_password_flow(policy: PasswordPolicy):
    """Handle the flow for generating a single password."""
    try:
        pwd = generate_password(policy)
        strength = evaluate_strength(pwd)
        print("\nGenerated Password:", pwd)
        print("Strength:", strength)
        print("-" * 40)
    except PasswordGeneratorError as e:
        print("Error:", e)


def generate_multiple_passwords_flow(policy: PasswordPolicy):
    """Handle the flow for generating multiple passwords at once."""
    count = get_int("How many passwords do you want to generate?", min_value=1, max_value=50)
    print("\nGenerated Passwords:")
    print("-" * 40)
    for i in range(1, count + 1):
        try:
            pwd = generate_password(policy)
            strength = evaluate_strength(pwd)
            print(f"{i}. {pwd}  (Strength: {strength})")
        except PasswordGeneratorError as e:
            print(f"{i}. Error generating password:", e)
    print("-" * 40)


def main_menu():
    """Main menu loop for the application."""
    print("====================================")
    print("     PYTHON PASSWORD GENERATOR      ")
    print("====================================")

    policy = PasswordPolicy()  # start with default policy

    while True:
        print("\nMain Menu")
        print("1. View current policy")
        print("2. Change policy")
        print("3. Generate a single password")
        print("4. Generate multiple passwords")
        print("5. Exit")

        choice = input("Enter your choice (1-5): ").strip()

        if choice == "1":
            print("\n--- Current Password Policy ---")
            print(f"Length         : {policy.length}")
            print(f"Lowercase (a-z): {policy.use_lowercase}")
            print(f"Uppercase (A-Z): {policy.use_uppercase}")
            print(f"Digits (0-9)   : {policy.use_digits}")
            print(f"Symbols        : {policy.use_symbols}")
            print("-" * 40)

        elif choice == "2":
            policy = prompt_for_policy()

        elif choice == "3":
            generate_single_password_flow(policy)

        elif choice == "4":
            generate_multiple_passwords_flow(policy)

        elif choice == "5":
            print("Exiting Password Generator. Goodbye!")
            break

        else:
            print("Invalid choice. Please select from 1 to 5.")


if __name__ == "__main__":
    main_menu()
