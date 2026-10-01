"""
authentication.py — PIN hashing, verification, and login logic.

Provides:
  • hash_pin()   — SHA-256 hash a PIN string (never store plain text)
  • verify_pin() — Compare a plain PIN against a stored hash
  • login()      — Full customer login flow with attempt limiting

NOTE: EDUCATIONAL SIMULATION — NOT a real banking system.
      In production, use bcrypt/scrypt/argon2 with salting.
      SHA-256 is used here for educational simplicity with
      only the standard library.
"""

import hashlib

from config import MAX_LOGIN_ATTEMPTS, STATUS_ACTIVE, STATUS_LOCKED


# ──────────────────────────────────────────────
# PIN Hashing & Verification
# ──────────────────────────────────────────────
def hash_pin(pin):
    """
    Return the SHA-256 hex digest of the given PIN string.

    In a real banking system, you would use a slow hashing
    algorithm with a unique salt (e.g., bcrypt). SHA-256 is
    used here because it is available in the standard library
    and is easy for students to understand.
    """
    return hashlib.sha256(pin.encode("utf-8")).hexdigest()


def verify_pin(plain_pin, stored_hash):
    """
    Hash the plain_pin and compare with the stored hash.
    Returns True if they match, False otherwise.
    """
    return hash_pin(plain_pin) == stored_hash


# ──────────────────────────────────────────────
# Login Flow
# ──────────────────────────────────────────────
def attempt_login(account_number, pin_entered):
    """
    Validate a customer login attempt.

    Steps:
      1. Check that the account exists.
      2. Check that the account is ACTIVE.
      3. Verify the PIN.
      4. Track failed attempts and lock after MAX_LOGIN_ATTEMPTS.

    Returns:
        (success: bool, message: str, account_info: dict or None)

    This function is separated from the UI so it can be tested
    independently. The caller handles display.
    """
    # Import here to avoid circular import at module level
    from database import (
        get_full_account_info,
        increment_failed_attempts,
        reset_failed_attempts,
        update_status
    )

    info = get_full_account_info(account_number)

    if not info:
        return False, "Account not found. Please check the account number.", None

    # Check account status
    status = info.get("status", "")
    if status == STATUS_LOCKED:
        return False, "This account is locked due to multiple failed login attempts. Contact admin.", None
    if status != STATUS_ACTIVE:
        return False, f"This account is currently {status}. Contact the bank.", None

    # Verify PIN
    if not verify_pin(pin_entered, info["pin_hash"]):
        # Increment failed attempts
        increment_failed_attempts(account_number)
        remaining = MAX_LOGIN_ATTEMPTS - (info["failed_attempts"] + 1)

        if remaining <= 0:
            update_status(account_number, STATUS_LOCKED)
            return False, "Account temporarily locked after too many failed attempts.", None

        return False, f"Incorrect PIN. {remaining} attempt(s) remaining.", None

    # Successful login — reset counter
    reset_failed_attempts(account_number)
    return True, f"Welcome, {info['name']}!", info
