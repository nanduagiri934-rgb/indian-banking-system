"""
admin.py — Administrator dashboard for the Indian Banking System.

Provides:
  • Admin login (username + password)
  • View all accounts
  • Search accounts (by number, name, mobile, customer ID)
  • View detailed account information
  • Freeze / Unfreeze accounts
  • View transactions for any account
  • Bank-wide statistics

NOTE: EDUCATIONAL SIMULATION — NOT a real banking system.
      Admin credentials are stored in config.py for simplicity.
"""

import hashlib

from config import (
    ADMIN_USERNAME, ADMIN_PASSWORD_HASH,
    SEPARATOR, THIN_SEP, STATUS_ACTIVE, STATUS_FROZEN
)
from database import (
    get_all_accounts, search_accounts, get_full_account_info,
    update_status, get_transactions, get_bank_statistics
)
from utils import (
    print_banner, print_success, print_error, print_info,
    print_warning, get_choice, press_enter, format_currency,
    mask_account_number, format_date, print_menu
)


# ──────────────────────────────────────────────
# Admin Login
# ──────────────────────────────────────────────
def admin_login():
    """
    Prompt for admin credentials and return True on success.
    Allows 3 attempts before returning False.
    """
    print_banner("ADMIN LOGIN")
    print_warning("Authorised personnel only.")
    print()

    for attempt in range(3):
        username = get_choice("  Username : ")
        password = get_choice("  Password : ")

        pw_hash = hashlib.sha256(password.encode()).hexdigest()

        if username == ADMIN_USERNAME and pw_hash == ADMIN_PASSWORD_HASH:
            print_success("Admin login successful.")
            return True
        else:
            remaining = 2 - attempt
            if remaining > 0:
                print_error(f"Invalid credentials. {remaining} attempt(s) remaining.")
            else:
                print_error("Access denied.")
    return False


# ──────────────────────────────────────────────
# Admin Dashboard
# ──────────────────────────────────────────────
def admin_dashboard():
    """Main admin menu loop."""
    while True:
        print_banner("ADMIN DASHBOARD")
        print_menu([
            "View All Accounts",
            "Search Account",
            "View Account Details",
            "Freeze / Unfreeze Account",
            "View Transactions",
            "Bank Statistics",
            "Logout"
        ])

        choice = get_choice("  Enter your choice: ")

        if choice == "1":
            _view_all_accounts()
        elif choice == "2":
            _search_account()
        elif choice == "3":
            _view_account_details()
        elif choice == "4":
            _freeze_unfreeze()
        elif choice == "5":
            _view_transactions()
        elif choice == "6":
            _bank_statistics()
        elif choice == "7":
            print_success("Admin logged out.")
            press_enter()
            break
        else:
            print_error("Invalid choice. Please try again.")
            press_enter()


# ──────────────────────────────────────────────
# View All Accounts
# ──────────────────────────────────────────────
def _view_all_accounts():
    """Display a table of every account in the system."""
    print_banner("ALL ACCOUNTS")
    accounts = get_all_accounts()

    if not accounts:
        print_info("No accounts found.")
        press_enter()
        return

    header = (f"  {'Cust ID':<12} {'Name':<18} {'Account No':<14} "
              f"{'Type':<10} {'Balance':>12} {'Status':<8}")
    print(header)
    print(f"  {THIN_SEP}")

    for acc in accounts:
        print(
            f"  {acc['customer_id']:<12} "
            f"{acc['name']:<18} "
            f"{acc['account_number']:<14} "
            f"{acc['account_type']:<10} "
            f"{format_currency(acc['balance']):>12} "
            f"{acc['status']:<8}"
        )

    print(f"\n  Total accounts: {len(accounts)}")
    print(SEPARATOR)
    press_enter()


# ──────────────────────────────────────────────
# Search Account
# ──────────────────────────────────────────────
def _search_account():
    """Search by account number, customer ID, name, or mobile."""
    print_banner("SEARCH ACCOUNT")
    keyword = get_choice("  Search (name / mobile / account no / cust ID): ")

    if not keyword.strip():
        print_error("Search term cannot be empty.")
        press_enter()
        return

    results = search_accounts(keyword.strip())

    if not results:
        print_info("No matching accounts found.")
        press_enter()
        return

    header = (f"  {'Account No':<14} {'Cust ID':<12} {'Name':<18} "
              f"{'Mobile':<12} {'Status':<8}")
    print(f"\n{header}")
    print(f"  {THIN_SEP}")

    for r in results:
        print(
            f"  {r['account_number']:<14} "
            f"{r['customer_id']:<12} "
            f"{r['name']:<18} "
            f"{r['mobile']:<12} "
            f"{r['status']:<8}"
        )

    print(f"\n  {len(results)} result(s) found.")
    print(SEPARATOR)
    press_enter()


# ──────────────────────────────────────────────
# View Account Details (Admin)
# ──────────────────────────────────────────────
def _view_account_details():
    """Show full details of a specific account (admin view)."""
    print_banner("ACCOUNT DETAILS (ADMIN)")
    acc_no = get_choice("  Enter Account Number: ")
    info = get_full_account_info(acc_no)

    if not info:
        print_error("Account not found.")
        press_enter()
        return

    print(f"\n  Customer Name    : {info['name']}")
    print(f"  Customer ID      : {info['customer_id']}")
    print(f"  Account Number   : {info['account_number']}")
    print(f"  Account Type     : {info['account_type']}")
    print(f"  Mobile           : {info['mobile']}")
    print(f"  Email            : {info['email']}")
    print(f"  DOB              : {info['dob']}")
    print(f"  Address          : {info['address']}")
    print(f"  City             : {info['city']}")
    print(f"  State            : {info['state']}")
    print(f"  Branch           : {info['branch']}")
    print(f"  IFSC             : {info['ifsc']}")
    print(f"  Status           : {info['status']}")
    print(f"  Failed Attempts  : {info['failed_attempts']}")
    print(f"  Opened On        : {format_date(info['created_at'])}")
    print(f"  Balance          : {format_currency(info['balance'])}")
    print(SEPARATOR)
    press_enter()


# ──────────────────────────────────────────────
# Freeze / Unfreeze Account
# ──────────────────────────────────────────────
def _freeze_unfreeze():
    """Toggle an account between ACTIVE and FROZEN."""
    print_banner("FREEZE / UNFREEZE ACCOUNT")
    acc_no = get_choice("  Enter Account Number: ")
    info = get_full_account_info(acc_no)

    if not info:
        print_error("Account not found.")
        press_enter()
        return

    current = info["status"]
    print(f"  Account: {acc_no}")
    print(f"  Name   : {info['name']}")
    print(f"  Status : {current}")
    print()

    if current == STATUS_ACTIVE:
        confirm = get_choice("  Freeze this account? (Y/N): ").upper()
        if confirm == "Y":
            update_status(acc_no, STATUS_FROZEN)
            print_success("Account has been FROZEN.")
        else:
            print_info("Operation cancelled.")
    elif current == STATUS_FROZEN:
        confirm = get_choice("  Unfreeze this account? (Y/N): ").upper()
        if confirm == "Y":
            update_status(acc_no, STATUS_ACTIVE)
            # Also reset failed attempts when unfreezing
            from database import reset_failed_attempts
            reset_failed_attempts(acc_no)
            print_success("Account has been UNFROZEN (ACTIVE).")
        else:
            print_info("Operation cancelled.")
    elif current == "LOCKED":
        confirm = get_choice("  Unlock this account? (Y/N): ").upper()
        if confirm == "Y":
            update_status(acc_no, STATUS_ACTIVE)
            from database import reset_failed_attempts
            reset_failed_attempts(acc_no)
            print_success("Account has been UNLOCKED (ACTIVE).")
        else:
            print_info("Operation cancelled.")
    else:
        print_warning(f"Account status '{current}' cannot be changed here.")

    press_enter()


# ──────────────────────────────────────────────
# View Transactions (Admin)
# ──────────────────────────────────────────────
def _view_transactions():
    """View transactions for any account."""
    print_banner("VIEW TRANSACTIONS (ADMIN)")
    acc_no = get_choice("  Enter Account Number: ")
    info = get_full_account_info(acc_no)

    if not info:
        print_error("Account not found.")
        press_enter()
        return

    txns = get_transactions(acc_no)
    if not txns:
        print_info("No transactions found for this account.")
        press_enter()
        return

    print(f"\n  Transactions for: {info['name']} ({acc_no})")
    header = (f"  {'Date':<12} {'Type':<12} {'Amount':>14} "
              f"{'Balance':>14} {'Status':<8}")
    print(header)
    print(f"  {THIN_SEP}")

    for txn in txns:
        date_str = format_date(txn["transaction_date"])
        amount = format_currency(txn["amount"])
        bal = format_currency(txn["balance_after"])
        print(
            f"  {date_str:<12} {txn['transaction_type']:<12} "
            f"{amount:>14} {bal:>14} {txn['status']:<8}"
        )

    print(SEPARATOR)
    press_enter()


# ──────────────────────────────────────────────
# Bank Statistics
# ──────────────────────────────────────────────
def _bank_statistics():
    """Display aggregate bank statistics."""
    print_banner("BANK STATISTICS")
    stats = get_bank_statistics()

    print(f"  Total Customers      : {stats['total_customers']}")
    print(f"  Active Accounts      : {stats['total_active']}")
    print(f"  Frozen Accounts      : {stats['total_frozen']}")
    print(f"  Locked Accounts      : {stats['total_locked']}")
    print(THIN_SEP)
    print(f"  Total Deposits       : {format_currency(stats['total_deposits'])}")
    print(f"  Total Withdrawals    : {format_currency(stats['total_withdrawals'])}")
    print(f"  Total Transfers      : {format_currency(stats['total_transfers'])}")
    print(THIN_SEP)
    print(f"  Total Bank Balance   : {format_currency(stats['total_balance'])}")
    print(SEPARATOR)
    press_enter()
