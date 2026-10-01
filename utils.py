"""
utils.py — Utility / helper functions for the Indian Banking System.

Contains reusable functions for:
  • Formatting currency in Indian Rupee style (₹1,23,456.00)
  • Generating unique IDs (account numbers, transaction IDs, etc.)
  • Displaying banners, menus, and messages
  • Masking sensitive data (account numbers, mobile numbers)
  • Date/time formatting

NOTE: EDUCATIONAL SIMULATION — NOT a real banking system.
"""

import random
import datetime
import uuid
import os

from config import (
    BANK_NAME, IFSC_PREFIX, BRANCH_CODE, SEPARATOR, THIN_SEP,
    ACCOUNT_NUMBER_LENGTH
)


# ──────────────────────────────────────────────
# Currency Formatting (Indian Numbering System)
# ──────────────────────────────────────────────
def format_currency(amount):
    """
    Format a number into Indian Rupee style.
    Example: 1234567.50 → ₹12,34,567.50

    Indian system groups the last 3 digits, then pairs of 2.
    """
    amount = round(amount, 2)
    is_negative = amount < 0
    amount = abs(amount)

    # Split into integer and decimal parts
    integer_part = int(amount)
    decimal_part = f"{amount:.2f}".split(".")[1]

    # Convert integer part to Indian grouping
    s = str(integer_part)
    if len(s) <= 3:
        formatted = s
    else:
        # Last 3 digits
        last_three = s[-3:]
        remaining = s[:-3]
        # Group remaining digits in pairs from the right
        groups = []
        while len(remaining) > 2:
            groups.append(remaining[-2:])
            remaining = remaining[:-2]
        if remaining:
            groups.append(remaining)
        groups.reverse()
        formatted = ",".join(groups) + "," + last_three

    result = f"₹{formatted}.{decimal_part}"
    if is_negative:
        result = f"-{result}"
    return result


# ──────────────────────────────────────────────
# Unique ID Generators
# ──────────────────────────────────────────────
def generate_account_number(existing_numbers):
    """
    Generate a unique 12-digit account number that does not
    collide with any number in `existing_numbers`.
    Uses `random.randint` for educational simplicity.
    """
    while True:
        number = "".join([str(random.randint(0, 9))
                          for _ in range(ACCOUNT_NUMBER_LENGTH)])
        # Ensure it doesn't start with 0 (looks more realistic)
        if number[0] == "0":
            continue
        if number not in existing_numbers:
            return number


def generate_customer_id():
    """
    Generate a customer ID like 'CUS100001' using UUID to
    guarantee uniqueness across sessions.
    """
    unique_part = uuid.uuid4().int % 900000 + 100000   # 6-digit number
    return f"CUS{unique_part}"


def generate_transaction_id():
    """
    Generate a transaction ID in the format: TXN + YYYYMMDD + 6 random digits.
    Example: TXN202610011234567
    """
    now = datetime.datetime.now()
    date_str = now.strftime("%Y%m%d")
    rand_part = str(random.randint(100000, 999999))
    return f"TXN{date_str}{rand_part}"


def generate_reference_number(mode="IMPS"):
    """
    Generate a transfer reference number.
    Example: IMPS20261001123456
    """
    now = datetime.datetime.now()
    date_str = now.strftime("%Y%m%d")
    rand_part = str(random.randint(100000, 999999))
    return f"{mode}{date_str}{rand_part}"


def generate_ifsc():
    """Return the IFSC code for the (single) branch."""
    return f"{IFSC_PREFIX}{BRANCH_CODE}"


# ──────────────────────────────────────────────
# Date / Time Helpers
# ──────────────────────────────────────────────
def current_timestamp():
    """Return the current date-time as an ISO string."""
    return datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")


def format_date(iso_string):
    """Convert 'YYYY-MM-DD ...' to Indian format 'DD-MM-YYYY'."""
    try:
        dt = datetime.datetime.strptime(iso_string[:10], "%Y-%m-%d")
        return dt.strftime("%d-%m-%Y")
    except (ValueError, TypeError):
        return iso_string


def format_datetime(iso_string):
    """Convert full timestamp to 'DD-MM-YYYY HH:MM:SS'."""
    try:
        dt = datetime.datetime.strptime(iso_string[:19], "%Y-%m-%d %H:%M:%S")
        return dt.strftime("%d-%m-%Y %H:%M:%S")
    except (ValueError, TypeError):
        return iso_string


# ──────────────────────────────────────────────
# Masking Helpers
# ──────────────────────────────────────────────
def mask_account_number(acc_no):
    """Mask an account number showing only the last 4 digits.
    Example: 458721963014 → ********3014
    """
    if len(acc_no) <= 4:
        return acc_no
    return "*" * (len(acc_no) - 4) + acc_no[-4:]


def mask_mobile(mobile):
    """Mask a mobile number showing only the last 4 digits.
    Example: 9876543210 → ******3210
    """
    if len(mobile) <= 4:
        return mobile
    return "*" * (len(mobile) - 4) + mobile[-4:]


# ──────────────────────────────────────────────
# Display Helpers
# ──────────────────────────────────────────────
def clear_screen():
    """Clear the terminal screen (works on Windows and Unix)."""
    os.system("cls" if os.name == "nt" else "clear")


def print_banner(title=""):
    """Print the bank's header banner."""
    print(f"\n{SEPARATOR}")
    print(f"  {BANK_NAME}".center(58))
    print("  EDUCATIONAL BANKING SIMULATION".center(58))
    if title:
        print(f"  {title}".center(58))
    print(SEPARATOR)


def print_success(message):
    """Print a success message."""
    print(f"\n  ✓ {message}")


def print_error(message):
    """Print an error message."""
    print(f"\n  ✗ {message}")


def print_info(message):
    """Print an informational message."""
    print(f"\n  ℹ {message}")


def print_warning(message):
    """Print a warning message."""
    print(f"\n  ⚠ {message}")


def print_menu(options):
    """
    Print a numbered menu from a list of option strings.
    Example: print_menu(["Create Account", "Login", "Exit"])
    """
    print()
    for i, option in enumerate(options, 1):
        print(f"  {i}. {option}")
    print()


def get_choice(prompt="  Enter your choice: "):
    """Prompt the user for input and return the stripped string."""
    try:
        return input(prompt).strip()
    except (EOFError, KeyboardInterrupt):
        print()
        return ""


def press_enter():
    """Pause until the user presses Enter."""
    input("\n  Press Enter to continue...")
