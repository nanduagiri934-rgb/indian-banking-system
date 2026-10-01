"""
models.py — Lightweight data models for the Indian Banking System.

This module defines simple classes that represent domain objects.
They are used as documentation of the data shapes and can be
expanded in future versions.

For this mini project, most data flows through dictionaries
returned by the SQLite row_factory.  These classes provide a
clear reference of what fields each entity contains.

NOTE: EDUCATIONAL SIMULATION — NOT a real banking system.
"""


class Customer:
    """
    Represents a bank customer's personal information.

    Attributes:
        customer_id (str): Unique customer identifier (e.g., CUS123456)
        name        (str): Full name of the customer
        mobile      (str): 10-digit Indian mobile number
        email       (str): Email address
        dob         (str): Date of birth (DD-MM-YYYY)
        address     (str): Street address
        city        (str): City name
        state       (str): Indian state / UT
    """

    def __init__(self, customer_id, name, mobile, email,
                 dob, address, city, state):
        self.customer_id = customer_id
        self.name = name
        self.mobile = mobile
        self.email = email
        self.dob = dob
        self.address = address
        self.city = city
        self.state = state

    def __repr__(self):
        return f"Customer({self.customer_id}, {self.name})"


class Account:
    """
    Represents a bank account linked to a Customer.

    Attributes:
        account_number  (str):   12-digit unique account number
        customer_id     (str):   FK to Customer
        account_type    (str):   'Savings' or 'Current'
        balance         (float): Current balance in ₹
        pin_hash        (str):   SHA-256 hash of the PIN
        ifsc            (str):   IFSC code of the branch
        branch          (str):   Branch name
        status          (str):   ACTIVE / FROZEN / LOCKED / CLOSED
        created_at      (str):   Account creation timestamp
        failed_attempts (int):   Consecutive failed login attempts
    """

    def __init__(self, account_number, customer_id, account_type,
                 balance, pin_hash, ifsc, branch, status,
                 created_at, failed_attempts=0):
        self.account_number = account_number
        self.customer_id = customer_id
        self.account_type = account_type
        self.balance = balance
        self.pin_hash = pin_hash
        self.ifsc = ifsc
        self.branch = branch
        self.status = status
        self.created_at = created_at
        self.failed_attempts = failed_attempts

    def __repr__(self):
        return f"Account({self.account_number}, {self.account_type})"


class Transaction:
    """
    Represents a single banking transaction.

    Attributes:
        transaction_id   (str):   Unique ID (e.g., TXN202610011234)
        account_number   (str):   Account involved
        transaction_type (str):   DEPOSIT / WITHDRAWAL / TRANSFER / RECEIVED / PIN_CHANGE
        amount           (float): Transaction amount in ₹
        description      (str):   Human-readable description
        reference_number (str):   Reference / UTR number
        transaction_date (str):   Timestamp of the transaction
        balance_after    (float): Account balance after this transaction
        status           (str):   SUCCESS / FAILED / PENDING
    """

    def __init__(self, transaction_id, account_number, transaction_type,
                 amount, description, reference_number,
                 transaction_date, balance_after, status="SUCCESS"):
        self.transaction_id = transaction_id
        self.account_number = account_number
        self.transaction_type = transaction_type
        self.amount = amount
        self.description = description
        self.reference_number = reference_number
        self.transaction_date = transaction_date
        self.balance_after = balance_after
        self.status = status

    def __repr__(self):
        return f"Transaction({self.transaction_id}, {self.transaction_type}, ₹{self.amount})"
