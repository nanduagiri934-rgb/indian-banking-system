"""
config.py — Configuration constants for the Indian Banking System.

This module stores all the configurable values used across the project,
such as bank name, branch info, IFSC prefix, limits, and admin credentials.

NOTE: This is an EDUCATIONAL SIMULATION — NOT a real banking system.
      Admin credentials here are for demonstration only.
"""

import hashlib
import os

# ──────────────────────────────────────────────
# Bank Information (Fictional)
# ──────────────────────────────────────────────
BANK_NAME = "Bharat National Bank"
BANK_SHORT = "BNB"
IFSC_PREFIX = "BNBK0"           # First 5 chars of IFSC code
BRANCH_NAME = "Hyderabad Main Branch"
BRANCH_CODE = "001234"          # Used in IFSC generation

# ──────────────────────────────────────────────
# Account Settings
# ──────────────────────────────────────────────
ACCOUNT_NUMBER_LENGTH = 12      # Standard 12-digit account number
MIN_OPENING_BALANCE = 1000.00   # ₹1,000 minimum opening balance
MIN_BALANCE_SAVINGS = 500.00    # Minimum balance for savings account
MIN_BALANCE_CURRENT = 5000.00   # Minimum balance for current account

# ──────────────────────────────────────────────
# PIN Settings
# ──────────────────────────────────────────────
PIN_LENGTHS = [4, 6]            # Allowed PIN lengths (4-digit or 6-digit)
MAX_LOGIN_ATTEMPTS = 3          # Lock account after this many failures

# ──────────────────────────────────────────────
# Transaction Limits (per transaction)
# ──────────────────────────────────────────────
MAX_DEPOSIT = 500000.00         # ₹5,00,000
MAX_WITHDRAWAL = 200000.00     # ₹2,00,000
MAX_TRANSFER = 200000.00       # ₹2,00,000

# ──────────────────────────────────────────────
# Transfer Modes (Simulated)
# ──────────────────────────────────────────────
TRANSFER_MODES = {
    "1": "UPI",
    "2": "IMPS",
    "3": "NEFT"
}

# ──────────────────────────────────────────────
# Account Types
# ──────────────────────────────────────────────
ACCOUNT_TYPES = {
    "1": "Savings",
    "2": "Current"
}

# ──────────────────────────────────────────────
# Account Statuses
# ──────────────────────────────────────────────
STATUS_ACTIVE = "ACTIVE"
STATUS_FROZEN = "FROZEN"
STATUS_LOCKED = "LOCKED"
STATUS_CLOSED = "CLOSED"

# ──────────────────────────────────────────────
# Database
# ──────────────────────────────────────────────
DATABASE_DIR = "data"
DATABASE_NAME = "bank.db"

# ──────────────────────────────────────────────
# Admin Credentials (Educational Demo Only)
# The password hash below is for: admin1234
# In a real system, credentials would NEVER be
# stored in source code.
# ──────────────────────────────────────────────
ADMIN_USERNAME = "admin"
ADMIN_PASSWORD_HASH = hashlib.sha256("admin1234".encode()).hexdigest()

# ──────────────────────────────────────────────
# Display Settings
# ──────────────────────────────────────────────
SEPARATOR = "=" * 58
THIN_SEP = "-" * 58
MINI_STATEMENT_COUNT = 5        # Number of transactions in mini statement

# ──────────────────────────────────────────────
# Indian States (for validation / display)
# ──────────────────────────────────────────────
INDIAN_STATES = [
    "Andhra Pradesh", "Arunachal Pradesh", "Assam", "Bihar",
    "Chhattisgarh", "Goa", "Gujarat", "Haryana", "Himachal Pradesh",
    "Jharkhand", "Karnataka", "Kerala", "Madhya Pradesh",
    "Maharashtra", "Manipur", "Meghalaya", "Mizoram", "Nagaland",
    "Odisha", "Punjab", "Rajasthan", "Sikkim", "Tamil Nadu",
    "Telangana", "Tripura", "Uttar Pradesh", "Uttarakhand",
    "West Bengal", "Delhi", "Chandigarh", "Puducherry",
    "Jammu and Kashmir", "Ladakh"
]
