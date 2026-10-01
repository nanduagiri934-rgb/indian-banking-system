"""
database.py — SQLite database layer for the Indian Banking System.

Responsibilities:
  • Create / connect to the SQLite database file
  • Create tables (customers, accounts, transactions)
  • Provide helper functions for CRUD operations
  • Seed sample data for demonstration

Tables:
  customers  — personal information (name, mobile, email, …)
  accounts   — banking details (balance, PIN hash, status, …)
  transactions — full transaction history

NOTE: EDUCATIONAL SIMULATION — NOT a real banking system.
"""

import sqlite3
import os

from config import (
    DATABASE_DIR, DATABASE_NAME, STATUS_ACTIVE,
    MIN_OPENING_BALANCE, BRANCH_NAME
)
from utils import (
    generate_account_number, generate_customer_id,
    generate_ifsc, current_timestamp, generate_transaction_id,
    generate_reference_number
)
from authentication import hash_pin


# ──────────────────────────────────────────────
# Database Path
# ──────────────────────────────────────────────
def _db_path():
    """Return the absolute path to the SQLite database file."""
    # Determine the directory where this script lives
    base_dir = os.path.dirname(os.path.abspath(__file__))
    data_dir = os.path.join(base_dir, DATABASE_DIR)
    os.makedirs(data_dir, exist_ok=True)
    return os.path.join(data_dir, DATABASE_NAME)


def get_connection():
    """Open and return a new SQLite connection with row_factory."""
    conn = sqlite3.connect(_db_path())
    conn.row_factory = sqlite3.Row          # Access columns by name
    conn.execute("PRAGMA foreign_keys = ON") # Enforce FK constraints
    return conn


# ──────────────────────────────────────────────
# Table Creation
# ──────────────────────────────────────────────
def initialize_database():
    """
    Create all required tables if they do not exist.
    Called once when the application starts.
    """
    conn = get_connection()
    cursor = conn.cursor()

    # --- customers table ---
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS customers (
            customer_id   TEXT PRIMARY KEY,
            name          TEXT NOT NULL,
            mobile        TEXT NOT NULL,
            email         TEXT NOT NULL,
            dob           TEXT NOT NULL,
            address       TEXT NOT NULL,
            city          TEXT NOT NULL,
            state         TEXT NOT NULL
        )
    """)

    # --- accounts table ---
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS accounts (
            account_number  TEXT PRIMARY KEY,
            customer_id     TEXT NOT NULL,
            account_type    TEXT NOT NULL,
            balance         REAL NOT NULL DEFAULT 0.0,
            pin_hash        TEXT NOT NULL,
            ifsc            TEXT NOT NULL,
            branch          TEXT NOT NULL,
            status          TEXT NOT NULL DEFAULT 'ACTIVE',
            created_at      TEXT NOT NULL,
            failed_attempts INTEGER NOT NULL DEFAULT 0,
            FOREIGN KEY (customer_id) REFERENCES customers(customer_id)
        )
    """)

    # --- transactions table ---
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS transactions (
            transaction_id    TEXT PRIMARY KEY,
            account_number    TEXT NOT NULL,
            transaction_type  TEXT NOT NULL,
            amount            REAL NOT NULL,
            description       TEXT,
            reference_number  TEXT,
            transaction_date  TEXT NOT NULL,
            balance_after     REAL NOT NULL,
            status            TEXT NOT NULL DEFAULT 'SUCCESS',
            FOREIGN KEY (account_number) REFERENCES accounts(account_number)
        )
    """)

    conn.commit()
    conn.close()


# ──────────────────────────────────────────────
# Customer & Account Queries
# ──────────────────────────────────────────────
def get_all_account_numbers():
    """Return a set of all existing account numbers."""
    conn = get_connection()
    rows = conn.execute("SELECT account_number FROM accounts").fetchall()
    conn.close()
    return {row["account_number"] for row in rows}


def create_customer_and_account(name, mobile, email, dob, address,
                                city, state, account_type, pin):
    """
    Insert a new customer and associated account.
    Returns (customer_id, account_number) on success.
    """
    customer_id = generate_customer_id()
    existing = get_all_account_numbers()
    account_number = generate_account_number(existing)
    ifsc = generate_ifsc()
    pin_hashed = hash_pin(pin)
    now = current_timestamp()

    conn = get_connection()
    try:
        conn.execute(
            """INSERT INTO customers
               (customer_id, name, mobile, email, dob, address, city, state)
               VALUES (?, ?, ?, ?, ?, ?, ?, ?)""",
            (customer_id, name, mobile, email, dob, address, city, state)
        )
        conn.execute(
            """INSERT INTO accounts
               (account_number, customer_id, account_type, balance,
                pin_hash, ifsc, branch, status, created_at, failed_attempts)
               VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""",
            (account_number, customer_id, account_type,
             MIN_OPENING_BALANCE, pin_hashed, ifsc, BRANCH_NAME,
             STATUS_ACTIVE, now, 0)
        )

        # Record the opening balance as a DEPOSIT transaction
        txn_id = generate_transaction_id()
        ref = generate_reference_number("OPEN")
        conn.execute(
            """INSERT INTO transactions
               (transaction_id, account_number, transaction_type, amount,
                description, reference_number, transaction_date,
                balance_after, status)
               VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)""",
            (txn_id, account_number, "DEPOSIT", MIN_OPENING_BALANCE,
             "Opening balance deposit", ref, now, MIN_OPENING_BALANCE,
             "SUCCESS")
        )

        conn.commit()
        return customer_id, account_number
    except sqlite3.Error as e:
        conn.rollback()
        raise e
    finally:
        conn.close()


def get_account_by_number(account_number):
    """Fetch an account row by its account number (or None)."""
    conn = get_connection()
    row = conn.execute(
        "SELECT * FROM accounts WHERE account_number = ?",
        (account_number,)
    ).fetchone()
    conn.close()
    return dict(row) if row else None


def get_customer_by_id(customer_id):
    """Fetch a customer row by customer_id (or None)."""
    conn = get_connection()
    row = conn.execute(
        "SELECT * FROM customers WHERE customer_id = ?",
        (customer_id,)
    ).fetchone()
    conn.close()
    return dict(row) if row else None


def get_full_account_info(account_number):
    """
    Return a merged dictionary with both customer + account fields,
    or None if the account does not exist.
    """
    account = get_account_by_number(account_number)
    if not account:
        return None
    customer = get_customer_by_id(account["customer_id"])
    if not customer:
        return None
    return {**customer, **account}


def update_account_field(account_number, field, value):
    """Update a single field in the accounts table."""
    conn = get_connection()
    conn.execute(
        f"UPDATE accounts SET {field} = ? WHERE account_number = ?",
        (value, account_number)
    )
    conn.commit()
    conn.close()


def update_balance(account_number, new_balance):
    """Shortcut to update the balance column."""
    update_account_field(account_number, "balance", round(new_balance, 2))


def update_pin(account_number, new_pin_hash):
    """Update the stored PIN hash for an account."""
    update_account_field(account_number, "pin_hash", new_pin_hash)


def update_status(account_number, new_status):
    """Update account status (ACTIVE / FROZEN / LOCKED)."""
    update_account_field(account_number, "status", new_status)


def increment_failed_attempts(account_number):
    """Increment the failed login attempt counter by 1."""
    conn = get_connection()
    conn.execute(
        """UPDATE accounts
           SET failed_attempts = failed_attempts + 1
           WHERE account_number = ?""",
        (account_number,)
    )
    conn.commit()
    conn.close()


def reset_failed_attempts(account_number):
    """Reset the failed attempt counter to 0 (after successful login)."""
    update_account_field(account_number, "failed_attempts", 0)


# ──────────────────────────────────────────────
# Transaction Queries
# ──────────────────────────────────────────────
def insert_transaction(account_number, txn_type, amount, description,
                       reference, balance_after, status="SUCCESS"):
    """Insert a single transaction record."""
    txn_id = generate_transaction_id()
    now = current_timestamp()
    conn = get_connection()
    conn.execute(
        """INSERT INTO transactions
           (transaction_id, account_number, transaction_type, amount,
            description, reference_number, transaction_date,
            balance_after, status)
           VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)""",
        (txn_id, account_number, txn_type, amount,
         description, reference, now, balance_after, status)
    )
    conn.commit()
    conn.close()
    return txn_id


def get_transactions(account_number, limit=None):
    """
    Return a list of transaction dicts for an account,
    ordered newest-first.  Use limit to restrict count.
    """
    conn = get_connection()
    query = """SELECT * FROM transactions
               WHERE account_number = ?
               ORDER BY transaction_date DESC"""
    if limit:
        query += f" LIMIT {int(limit)}"
    rows = conn.execute(query, (account_number,)).fetchall()
    conn.close()
    return [dict(r) for r in rows]


# ──────────────────────────────────────────────
# Transfer (Atomic Two-Account Update)
# ──────────────────────────────────────────────
def execute_transfer(sender_acc, receiver_acc, amount, mode):
    """
    Perform an atomic transfer:
      1. Debit sender
      2. Credit receiver
      3. Record both transactions

    Uses a single SQLite transaction so that a failure
    in any step rolls back all changes (atomicity).
    """
    conn = get_connection()
    try:
        cursor = conn.cursor()
        now = current_timestamp()
        ref = generate_reference_number(mode)
        sender_txn_id = generate_transaction_id()
        receiver_txn_id = generate_transaction_id()

        # Fetch current balances inside the transaction
        sender = cursor.execute(
            "SELECT balance FROM accounts WHERE account_number = ?",
            (sender_acc,)
        ).fetchone()
        receiver = cursor.execute(
            "SELECT balance FROM accounts WHERE account_number = ?",
            (receiver_acc,)
        ).fetchone()

        if not sender or not receiver:
            raise ValueError("Account not found during transfer.")

        new_sender_bal = round(sender["balance"] - amount, 2)
        new_receiver_bal = round(receiver["balance"] + amount, 2)

        # Update balances
        cursor.execute(
            "UPDATE accounts SET balance = ? WHERE account_number = ?",
            (new_sender_bal, sender_acc)
        )
        cursor.execute(
            "UPDATE accounts SET balance = ? WHERE account_number = ?",
            (new_receiver_bal, receiver_acc)
        )

        # Sender transaction (DEBIT)
        cursor.execute(
            """INSERT INTO transactions
               (transaction_id, account_number, transaction_type, amount,
                description, reference_number, transaction_date,
                balance_after, status)
               VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)""",
            (sender_txn_id, sender_acc, "TRANSFER", amount,
             f"{mode} transfer to {receiver_acc}", ref, now,
             new_sender_bal, "SUCCESS")
        )

        # Receiver transaction (CREDIT)
        cursor.execute(
            """INSERT INTO transactions
               (transaction_id, account_number, transaction_type, amount,
                description, reference_number, transaction_date,
                balance_after, status)
               VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)""",
            (receiver_txn_id, receiver_acc, "RECEIVED", amount,
             f"{mode} received from {sender_acc}", ref, now,
             new_receiver_bal, "SUCCESS")
        )

        conn.commit()
        return sender_txn_id, ref, new_sender_bal

    except Exception as e:
        conn.rollback()
        raise e
    finally:
        conn.close()


# ──────────────────────────────────────────────
# Admin Queries
# ──────────────────────────────────────────────
def get_all_accounts():
    """Return a list of all account+customer rows (for admin view)."""
    conn = get_connection()
    rows = conn.execute("""
        SELECT a.account_number, a.customer_id, c.name,
               a.account_type, a.balance, a.status
        FROM accounts a
        JOIN customers c ON a.customer_id = c.customer_id
        ORDER BY c.name
    """).fetchall()
    conn.close()
    return [dict(r) for r in rows]


def search_accounts(keyword):
    """
    Search accounts by account_number, customer_id, name, or mobile.
    Returns matching rows.
    """
    conn = get_connection()
    like = f"%{keyword}%"
    rows = conn.execute("""
        SELECT a.account_number, a.customer_id, c.name,
               c.mobile, a.account_type, a.balance, a.status
        FROM accounts a
        JOIN customers c ON a.customer_id = c.customer_id
        WHERE a.account_number LIKE ?
           OR a.customer_id LIKE ?
           OR c.name LIKE ?
           OR c.mobile LIKE ?
        ORDER BY c.name
    """, (like, like, like, like)).fetchall()
    conn.close()
    return [dict(r) for r in rows]


def get_bank_statistics():
    """
    Compute bank-wide statistics for the admin dashboard.
    Returns a dictionary.
    """
    conn = get_connection()
    stats = {}

    stats["total_customers"] = conn.execute(
        "SELECT COUNT(*) FROM customers"
    ).fetchone()[0]

    stats["total_active"] = conn.execute(
        "SELECT COUNT(*) FROM accounts WHERE status = 'ACTIVE'"
    ).fetchone()[0]

    stats["total_frozen"] = conn.execute(
        "SELECT COUNT(*) FROM accounts WHERE status = 'FROZEN'"
    ).fetchone()[0]

    stats["total_locked"] = conn.execute(
        "SELECT COUNT(*) FROM accounts WHERE status = 'LOCKED'"
    ).fetchone()[0]

    row = conn.execute(
        "SELECT COALESCE(SUM(amount), 0) FROM transactions WHERE transaction_type = 'DEPOSIT'"
    ).fetchone()
    stats["total_deposits"] = row[0]

    row = conn.execute(
        "SELECT COALESCE(SUM(amount), 0) FROM transactions WHERE transaction_type = 'WITHDRAWAL'"
    ).fetchone()
    stats["total_withdrawals"] = row[0]

    row = conn.execute(
        "SELECT COALESCE(SUM(amount), 0) FROM transactions WHERE transaction_type = 'TRANSFER'"
    ).fetchone()
    stats["total_transfers"] = row[0]

    row = conn.execute(
        "SELECT COALESCE(SUM(balance), 0) FROM accounts"
    ).fetchone()
    stats["total_balance"] = row[0]

    conn.close()
    return stats


# ──────────────────────────────────────────────
# Sample / Demo Data
# ──────────────────────────────────────────────
def seed_sample_data():
    """
    Insert two demo accounts if the database is empty.
    This makes it easy to demonstrate transfers immediately.
    Uses fictional Indian names and information.
    """
    conn = get_connection()
    count = conn.execute("SELECT COUNT(*) FROM accounts").fetchone()[0]
    conn.close()

    if count > 0:
        return  # Data already exists — skip seeding

    # Sample customer 1
    create_customer_and_account(
        name="Rahul Kumar",
        mobile="9876543210",
        email="rahul.kumar@example.com",
        dob="15-08-1995",
        address="42 MG Road",
        city="Hyderabad",
        state="Telangana",
        account_type="Savings",
        pin="1234"
    )

    # Sample customer 2
    create_customer_and_account(
        name="Priya Sharma",
        mobile="8765432109",
        email="priya.sharma@example.com",
        dob="22-01-1998",
        address="18 Anna Salai",
        city="Chennai",
        state="Tamil Nadu",
        account_type="Savings",
        pin="5678"
    )

    # Give them some initial balance for demo purposes
    accounts = get_all_accounts()
    for acc in accounts:
        conn = get_connection()
        conn.execute(
            "UPDATE accounts SET balance = ? WHERE account_number = ?",
            (25000.00, acc["account_number"])
        )
        conn.commit()
        conn.close()
        # Update the opening transaction's balance_after too
        conn = get_connection()
        conn.execute(
            """UPDATE transactions SET balance_after = ?
               WHERE account_number = ? AND transaction_type = 'DEPOSIT'""",
            (25000.00, acc["account_number"])
        )
        conn.commit()
        conn.close()
