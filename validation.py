"""
validation.py — Input validation helpers for the Indian Banking System.

Validates:
  • Indian mobile numbers (10 digits, starts with 6-9)
  • Email addresses (basic regex)
  • PINs (4 or 6 digits)
  • Monetary amounts (positive, within limits)
  • Names, account numbers, and other text fields

NOTE: EDUCATIONAL SIMULATION — NOT a real banking system.
"""

import re
from config import (
    PIN_LENGTHS, MAX_DEPOSIT, MAX_WITHDRAWAL, MAX_TRANSFER
)


# ──────────────────────────────────────────────
# Name Validation
# ──────────────────────────────────────────────
def validate_name(name):
    """
    Validate a customer name.
    Rules:
      - Not empty
      - At least 2 characters
      - Only letters and spaces
    Returns (is_valid: bool, error_message: str).
    """
    if not name or not name.strip():
        return False, "Name cannot be empty."
    name = name.strip()
    if len(name) < 2:
        return False, "Name must be at least 2 characters."
    if not re.match(r"^[A-Za-z ]+$", name):
        return False, "Name must contain only letters and spaces."
    return True, ""


# ──────────────────────────────────────────────
# Mobile Number Validation
# ──────────────────────────────────────────────
def validate_mobile(mobile):
    """
    Validate an Indian mobile number.
    Rules:
      - Exactly 10 digits
      - Must start with 6, 7, 8, or 9
    """
    if not mobile:
        return False, "Mobile number cannot be empty."
    if not re.match(r"^[6-9]\d{9}$", mobile):
        return False, "Enter a valid 10-digit Indian mobile number (starts with 6-9)."
    return True, ""


# ──────────────────────────────────────────────
# Email Validation
# ──────────────────────────────────────────────
def validate_email(email):
    """
    Basic email validation using a simple regex.
    Not RFC-compliant, but sufficient for an educational project.
    """
    if not email:
        return False, "Email cannot be empty."
    pattern = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
    if not re.match(pattern, email):
        return False, "Enter a valid email address."
    return True, ""


# ──────────────────────────────────────────────
# Date of Birth Validation
# ──────────────────────────────────────────────
def validate_dob(dob):
    """
    Validate date of birth in DD-MM-YYYY format.
    The person must be at least 18 years old.
    """
    import datetime

    if not dob:
        return False, "Date of birth cannot be empty."
    try:
        birth_date = datetime.datetime.strptime(dob, "%d-%m-%Y")
    except ValueError:
        return False, "Enter date in DD-MM-YYYY format."

    today = datetime.date.today()
    age = (today - birth_date.date()).days // 365
    if age < 18:
        return False, "Customer must be at least 18 years old."
    if age > 120:
        return False, "Please enter a valid date of birth."
    return True, ""


# ──────────────────────────────────────────────
# PIN Validation
# ──────────────────────────────────────────────
def validate_pin(pin):
    """
    Validate that a PIN is either 4 or 6 digits.
    """
    if not pin:
        return False, "PIN cannot be empty."
    if not pin.isdigit():
        return False, "PIN must contain only digits."
    if len(pin) not in PIN_LENGTHS:
        return False, f"PIN must be {' or '.join(str(l) for l in PIN_LENGTHS)} digits."
    return True, ""


# ──────────────────────────────────────────────
# Amount Validation
# ──────────────────────────────────────────────
def validate_amount(amount_str, max_limit=None, label="Amount"):
    """
    Validate a monetary amount string.
    Returns (is_valid, amount_float, error_message).
    """
    if not amount_str:
        return False, 0, f"{label} cannot be empty."
    try:
        amount = float(amount_str)
    except ValueError:
        return False, 0, f"{label} must be a valid number."

    if amount <= 0:
        return False, 0, f"{label} must be greater than zero."

    # Check for more than 2 decimal places
    if "." in amount_str and len(amount_str.split(".")[-1]) > 2:
        return False, 0, f"{label} can have at most 2 decimal places."

    if max_limit and amount > max_limit:
        from utils import format_currency
        return False, 0, f"{label} cannot exceed {format_currency(max_limit)} per transaction."

    return True, round(amount, 2), ""


# ──────────────────────────────────────────────
# Account Number Validation (format only)
# ──────────────────────────────────────────────
def validate_account_number(acc_no):
    """Validate that the account number is a 12-digit numeric string."""
    if not acc_no:
        return False, "Account number cannot be empty."
    if not acc_no.isdigit() or len(acc_no) != 12:
        return False, "Account number must be exactly 12 digits."
    return True, ""


# ──────────────────────────────────────────────
# Address Validation
# ──────────────────────────────────────────────
def validate_address(address):
    """Basic non-empty address validation."""
    if not address or not address.strip():
        return False, "Address cannot be empty."
    if len(address.strip()) < 5:
        return False, "Address must be at least 5 characters."
    return True, ""


def validate_city(city):
    """Basic non-empty city validation."""
    if not city or not city.strip():
        return False, "City cannot be empty."
    if not re.match(r"^[A-Za-z ]+$", city.strip()):
        return False, "City must contain only letters and spaces."
    return True, ""
