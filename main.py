"""
Simple Password Generator 

Features:
- Menu-driven interface
- Customizable password policy (length, allowed character types)
- Generate one or many passwords at a time
- Rough password strength checker
"""

import string
import secrets
from dataclasses import dataclass


# You can tweak this if you want a different symbol set
SYMBOLS = "!@#$%^&*()-_=+[]{};:,.<>?/"


@dataclass
class PasswordPolicy:
    length: int = 12
    use_lowercase: bool = True
    use_uppercase: bool = True
    use_digits: bool = True
    use_symbols: bool = True


class PasswordGeneratorError(Exception):
    """Custom exception for password generator related issues."""
    pass


def build_character_pool(policy: PasswordPolicy) -> str:
    """
    Build the pool of characters according to the given policy.

    Raises:
        PasswordGeneratorError: If no character types are enabled.
    """
    pool_parts = []

    if policy.use_lowercase:
        pool_parts.append(string.ascii_lowercase)
    if policy.use_uppercase:
        pool_parts.append(string.ascii_uppercase)
    if policy.use_digits:
        pool_parts.append(string.digits)
    if policy.use_symbols:
        pool_parts.append(SYMBOLS)

    if not pool_parts:
        raise PasswordGeneratorError(
            "No character types selected. "
            "Please enable at least one character category."
        )

    return "".join(pool_parts)


def generate_password(policy: PasswordPolicy) -> str:
    """
    Generate a single password that follows the given policy.

    We try to guarantee at least one of each selected character type
    (lowercase, uppercase, digits, symbols) for better strength.
    """
    if policy.length <= 0:
        raise PasswordGeneratorError("Password length must be a positive integer.")

    pool = build_character_pool(policy)
    password_chars = []

    # Ensure at least one character from each enabled category
    if policy.use_lowercase:
        password_chars.append(secrets.choice(string.ascii_lowercase))
    if policy.use_uppercase:
        password_chars.append(secrets.choice(string.ascii_uppercase))
    if policy.use_digits:
        password_chars.append(secrets.choice(string.digits))
    if policy.use_symbols:
        password_chars.append(secrets.choice(SYMBOLS))

    # Fill the remaining characters from the full pool
    while len(password_chars) < policy.length:
        password_chars.append(secrets.choice(pool))

    # Shuffle the list in-place using random indices (still using secrets)
    for i in range(len(password_chars)):
        j = secrets.randbelow(len(password_chars))
        password_chars[i], password_chars[j] = password_chars[j], password_chars[i]

    return "".join(password_chars)


def evaluate_strength(password: str) -> str:
    """
    Very simple strength estimator.

    This is not cryptographically accurate, it's just a rough idea
    based on length and variety of character types.
    """
    length_score = len(password)

    has_lower = any(c.islower() for c in password)
    has_upper = any(c.isupper() for c in password)
    has_digit = any(c.isdigit() for c in password)
    has_symbol = any(c in SYMBOLS for c in password)

    variety_score = sum([has_lower, has_upper, has_digit, has_symbol])

    # Simple scoring rule: length + 2 * variety
    total_score = length_score + (2 * variety_score)

    if total_score < 10:
        return "Weak"
    elif total_score < 18:
        return "Moderate"
    elif total_score < 26:
        return "Strong"
    else:
        return "Very Strong"


def get_yes_no(prompt: str) -> bool:
    """
    Ask the user a yes/no question and return True/False.

    Keeps asking until the user types something valid.
    """
    while True:
        ans = input(prompt + " (y/n): ").strip().lower()
        if ans in ("y", "yes"):
            return True
        if ans in ("n", "no"):
            return False
        print("Invalid input. Please type 'y' or 'n'.")


def get_int(prompt: str, min_value: int | None = None, max_value: int | None = None) -> int:
    """
    Ask the user for an integer, with optional min/max validation.
    """
    while True:
        raw = input(prompt + ": ").strip()

        if not raw.isdigit():
            print("Please enter a valid positive integer.")
            continue

        value = int(raw)

        if min_value is not None and value < min_value:
            print(f"Please enter a value >= {min_value}.")
            continue

        if max_value is not None and value > max_value:
            print(f"Please enter a value <= {max_value}.")
            continue

        return value


def prompt_for_policy() -> PasswordPolicy:
    """
    Interactive dialog to let the user configure a password policy.
    """
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

    # Safety check: don't allow a policy with no character types at all
    if not any([
        policy.use_lowercase,
        policy.use_uppercase,
        policy.use_digits,
        policy.use_symbols,
    ]):
        print("You must select at least one character type.")
        print("Reverting to default policy with the chosen length.")
        policy = PasswordPolicy(length=length)

    return policy


def generate_single_password_flow(policy: PasswordPolicy) -> None:
    """
    Flow helper: generate one password and display its strength.
    """
    try:
        pwd = generate_password(policy)
        strength = evaluate_strength(pwd)

        print("\nGenerated Password:", pwd)
        print("Strength:", strength)
        print("-" * 40)
    except PasswordGeneratorError as exc:
        print("Error:", exc)


def generate_multiple_passwords_flow(policy: PasswordPolicy) -> None:
    """
    Flow helper: generate several passwords and print them one by one.
    """
    count = get_int(
        "How many passwords do you want to generate?",
        min_value=1,
        max_value=50,
    )

    print("\nGenerated Passwords:")
    print("-" * 40)

    for idx in range(1, count + 1):
        try:
            pwd = generate_password(policy)
            strength = evaluate_strength(pwd)
            print(f"{idx}. {pwd}  (Strength: {strength})")
        except PasswordGeneratorError as exc:
            print(f"{idx}. Error generating password:", exc)

    print("-" * 40)


def show_policy(policy: PasswordPolicy) -> None:
    """Print the current password policy in a readable format."""
    print("\n--- Current Password Policy ---")
    print(f"Length           : {policy.length}")
    print(f"Lowercase (a-z)  : {policy.use_lowercase}")
    print(f"Uppercase (A-Z)  : {policy.use_uppercase}")
    print(f"Digits (0-9)     : {policy.use_digits}")
    print(f"Symbols          : {policy.use_symbols}")
    print("-" * 40)


def main_menu() -> None:
    """
    Main loop of the program that shows the menu and responds to user commands.
    """
    print("====================================")
    print("        PYTHON PASSWORD TOOL        ")
    print("====================================")

    # Start with a default policy; user can change it later
    policy = PasswordPolicy()

    while True:
        print("\nMain Menu")
        print("1. View current policy")
        print("2. Change policy")
        print("3. Generate a single password")
        print("4. Generate multiple passwords")
        print("5. Exit")

        choice = input("Enter your choice (1-5): ").strip()

        if choice == "1":
            show_policy(policy)
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
            print("Invalid choice. Please select a number from 1 to 5.")


if __name__ == "__main__":
    main_menu()
