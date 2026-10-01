"""
transactions.py — Deposit, Withdrawal, Transfer, and History display.

Handles:
  • Depositing money into the logged-in account
  • Withdrawing money (with balance checks)
  • Transferring money to another account (atomic)
  • Displaying full transaction history
  • Displaying a mini statement (last N transactions)
  • Changing the account PIN

NOTE: EDUCATIONAL SIMULATION — NOT a real banking system.
"""

from config import (
    MAX_DEPOSIT, MAX_WITHDRAWAL, MAX_TRANSFER,
    TRANSFER_MODES, SEPARATOR, THIN_SEP,
    MINI_STATEMENT_COUNT, MIN_BALANCE_SAVINGS,
    MIN_BALANCE_CURRENT, PIN_LENGTHS
)
from validation import (
    validate_amount, validate_account_number, validate_pin
)
from database import (
    get_account_by_number, update_balance, insert_transaction,
    get_transactions, execute_transfer, get_full_account_info,
    update_pin as db_update_pin
)
from authentication import hash_pin, verify_pin
from utils import (
    print_banner, print_success, print_error, print_info,
    print_warning, get_choice, press_enter, format_currency,
    mask_account_number, format_date, format_datetime,
    generate_reference_number, print_menu
)


# ──────────────────────────────────────────────
# Check Balance
# ──────────────────────────────────────────────
def check_balance(info):
    """Display the current and available balance."""
    # Refresh balance from DB
    acc = get_account_by_number(info["account_number"])
    balance = acc["balance"]
    info["balance"] = balance  # keep session up to date

    print_banner("BALANCE ENQUIRY")
    print(f"  Account  : {mask_account_number(info['account_number'])}")
    print(f"  Balance  : {format_currency(balance)}")
    print(SEPARATOR)
    press_enter()


# ──────────────────────────────────────────────
# Deposit
# ──────────────────────────────────────────────
def deposit(info):
    """
    Deposit money into the logged-in account.
    Validates the amount, updates the balance, and records
    the transaction.
    """
    print_banner("DEPOSIT MONEY")
    print(f"  Account  : {mask_account_number(info['account_number'])}")
    print(f"  Balance  : {format_currency(info['balance'])}")
    print()

    amount_str = get_choice("  Enter deposit amount (₹): ")
    ok, amount, err = validate_amount(amount_str, MAX_DEPOSIT, "Deposit amount")
    if not ok:
        print_error(err)
        press_enter()
        return

    # Update balance
    new_balance = round(info["balance"] + amount, 2)
    update_balance(info["account_number"], new_balance)

    # Record transaction
    ref = generate_reference_number("DEP")
    txn_id = insert_transaction(
        account_number=info["account_number"],
        txn_type="DEPOSIT",
        amount=amount,
        description="Cash deposit",
        reference=ref,
        balance_after=new_balance
    )

    info["balance"] = new_balance  # update session

    # Display receipt
    print(f"\n{SEPARATOR}")
    print("  DEPOSIT SUCCESSFUL".center(58))
    print(SEPARATOR)
    print(f"  Transaction ID   : {txn_id}")
    print(f"  Type             : DEPOSIT")
    print(f"  Amount           : {format_currency(amount)}")
    print(f"  New Balance      : {format_currency(new_balance)}")
    print(f"  Status           : SUCCESS")
    print(SEPARATOR)
    press_enter()


# ──────────────────────────────────────────────
# Withdrawal
# ──────────────────────────────────────────────
def withdraw(info):
    """
    Withdraw money from the logged-in account.
    Checks for sufficient funds and minimum balance rules.
    """
    print_banner("WITHDRAW MONEY")
    print(f"  Account  : {mask_account_number(info['account_number'])}")
    print(f"  Balance  : {format_currency(info['balance'])}")
    print()

    amount_str = get_choice("  Enter withdrawal amount (₹): ")
    ok, amount, err = validate_amount(amount_str, MAX_WITHDRAWAL, "Withdrawal amount")
    if not ok:
        print_error(err)
        press_enter()
        return

    # Check minimum balance requirement
    min_bal = (MIN_BALANCE_CURRENT
               if info["account_type"] == "Current"
               else MIN_BALANCE_SAVINGS)

    if info["balance"] - amount < min_bal:
        print_error(
            f"Insufficient funds. Minimum balance of "
            f"{format_currency(min_bal)} must be maintained."
        )
        press_enter()
        return

    # Update balance
    new_balance = round(info["balance"] - amount, 2)
    update_balance(info["account_number"], new_balance)

    # Record transaction
    ref = generate_reference_number("WDL")
    txn_id = insert_transaction(
        account_number=info["account_number"],
        txn_type="WITHDRAWAL",
        amount=amount,
        description="Cash withdrawal",
        reference=ref,
        balance_after=new_balance
    )

    info["balance"] = new_balance

    print(f"\n{SEPARATOR}")
    print("  WITHDRAWAL SUCCESSFUL".center(58))
    print(SEPARATOR)
    print(f"  Transaction ID   : {txn_id}")
    print(f"  Type             : WITHDRAWAL")
    print(f"  Amount           : {format_currency(amount)}")
    print(f"  New Balance      : {format_currency(new_balance)}")
    print(f"  Status           : SUCCESS")
    print(SEPARATOR)
    press_enter()


# ──────────────────────────────────────────────
# Transfer
# ──────────────────────────────────────────────
def transfer(info):
    """
    Transfer money from the logged-in account to another
    account within the same bank (simulated IMPS/NEFT/UPI).
    Uses an atomic database transaction.
    """
    print_banner("TRANSFER MONEY")
    print(f"  Account  : {mask_account_number(info['account_number'])}")
    print(f"  Balance  : {format_currency(info['balance'])}")
    print()

    # Receiver account number
    receiver_acc = get_choice("  Receiver Account Number: ")
    ok, err = validate_account_number(receiver_acc)
    if not ok:
        print_error(err)
        press_enter()
        return

    # Check receiver exists
    receiver_info = get_account_by_number(receiver_acc)
    if not receiver_info:
        print_error("Receiver account not found.")
        press_enter()
        return

    # Cannot transfer to self
    if receiver_acc == info["account_number"]:
        print_error("Cannot transfer to your own account.")
        press_enter()
        return

    # Check receiver account is active
    if receiver_info["status"] != "ACTIVE":
        print_error("Receiver account is not active.")
        press_enter()
        return

    # Amount
    amount_str = get_choice("  Transfer Amount (₹)    : ")
    ok, amount, err = validate_amount(amount_str, MAX_TRANSFER, "Transfer amount")
    if not ok:
        print_error(err)
        press_enter()
        return

    # Minimum balance check
    min_bal = (MIN_BALANCE_CURRENT
               if info["account_type"] == "Current"
               else MIN_BALANCE_SAVINGS)
    if info["balance"] - amount < min_bal:
        print_error(
            f"Insufficient funds. Minimum balance of "
            f"{format_currency(min_bal)} must be maintained."
        )
        press_enter()
        return

    # Transfer mode
    print("\n  Transfer Mode:")
    print_menu(list(TRANSFER_MODES.values()))
    mode_choice = get_choice("  Select mode: ")
    mode = TRANSFER_MODES.get(mode_choice, "IMPS")

    # Fetch receiver name for confirmation
    receiver_full = get_full_account_info(receiver_acc)
    receiver_name = receiver_full["name"] if receiver_full else "Unknown"

    # Confirmation
    print(f"\n{THIN_SEP}")
    print(f"  Confirm Transfer Details:")
    print(f"  To      : {receiver_name} ({mask_account_number(receiver_acc)})")
    print(f"  Amount  : {format_currency(amount)}")
    print(f"  Mode    : {mode}")
    print(THIN_SEP)
    confirm = get_choice("  Proceed? (Y/N): ").upper()
    if confirm != "Y":
        print_info("Transfer cancelled.")
        press_enter()
        return

    # Execute atomic transfer
    try:
        txn_id, ref, new_balance = execute_transfer(
            sender_acc=info["account_number"],
            receiver_acc=receiver_acc,
            amount=amount,
            mode=mode
        )
    except Exception as e:
        print_error(f"Transfer failed: {e}")
        press_enter()
        return

    info["balance"] = new_balance

    print(f"\n{SEPARATOR}")
    print("  TRANSFER SUCCESSFUL".center(58))
    print(SEPARATOR)
    print(f"  Transaction ID   : {txn_id}")
    print(f"  Reference        : {ref}")
    print(f"  Amount           : {format_currency(amount)}")
    print(f"  Receiver         : {mask_account_number(receiver_acc)}")
    print(f"  Mode             : {mode}")
    print(f"  New Balance      : {format_currency(new_balance)}")
    print(f"  Status           : SUCCESS")
    print(SEPARATOR)
    press_enter()


# ──────────────────────────────────────────────
# Transaction History (Full)
# ──────────────────────────────────────────────
def transaction_history(info):
    """Display all transactions for the logged-in account."""
    print_banner("TRANSACTION HISTORY")

    txns = get_transactions(info["account_number"])
    if not txns:
        print_info("No transactions found.")
        press_enter()
        return

    _print_transaction_table(txns, info["account_number"])
    press_enter()


# ──────────────────────────────────────────────
# Mini Statement
# ──────────────────────────────────────────────
def mini_statement(info):
    """Display the last N transactions as a mini statement."""
    # Refresh balance
    acc = get_account_by_number(info["account_number"])
    balance = acc["balance"]
    info["balance"] = balance

    print_banner("MINI STATEMENT")
    print(f"  Account: {mask_account_number(info['account_number'])}")
    print()

    txns = get_transactions(info["account_number"],
                            limit=MINI_STATEMENT_COUNT)
    if not txns:
        print_info("No transactions found.")
        press_enter()
        return

    for txn in txns:
        date_str = format_date(txn["transaction_date"])
        txn_type = txn["transaction_type"]
        amount = txn["amount"]

        # Determine credit/debit sign
        if txn_type in ("DEPOSIT", "RECEIVED"):
            sign = "+"
        else:
            sign = "-"

        print(f"  {date_str}  {txn_type:<12}  {sign}{format_currency(amount)}")

    print(f"\n  Available Balance: {format_currency(balance)}")
    print(SEPARATOR)
    press_enter()


# ──────────────────────────────────────────────
# Change PIN
# ──────────────────────────────────────────────
def change_pin(info):
    """
    Allow the customer to change their PIN.
    Requires the current PIN for verification.
    """
    print_banner("CHANGE PIN")

    # Verify current PIN
    current = get_choice("  Enter current PIN : ")
    if not verify_pin(current, info["pin_hash"]):
        print_error("Current PIN is incorrect.")
        press_enter()
        return

    # New PIN
    while True:
        new_pin = get_choice("  Enter new PIN     : ")
        ok, err = validate_pin(new_pin)
        if not ok:
            print_error(err)
            continue

        if verify_pin(new_pin, info["pin_hash"]):
            print_error("New PIN must be different from current PIN.")
            continue

        confirm = get_choice("  Confirm new PIN   : ")
        if new_pin != confirm:
            print_error("PINs do not match. Try again.")
            continue
        break

    # Update in database
    new_hash = hash_pin(new_pin)
    db_update_pin(info["account_number"], new_hash)
    info["pin_hash"] = new_hash  # update session

    # Record in history
    ref = generate_reference_number("PIN")
    insert_transaction(
        account_number=info["account_number"],
        txn_type="PIN_CHANGE",
        amount=0,
        description="PIN changed successfully",
        reference=ref,
        balance_after=info["balance"]
    )

    print_success("PIN changed successfully.")
    press_enter()


# ──────────────────────────────────────────────
# Helper: Print Transaction Table
# ──────────────────────────────────────────────
def _print_transaction_table(txns, account_number):
    """
    Print transactions in a formatted table.
    """
    header = (f"  {'Date':<12} {'Type':<12} {'Amount':>14} "
              f"{'Cr/Dr':<8} {'Balance':>14}")
    print(header)
    print(f"  {THIN_SEP}")

    for txn in txns:
        date_str = format_date(txn["transaction_date"])
        txn_type = txn["transaction_type"]
        amount = format_currency(txn["amount"])
        bal = format_currency(txn["balance_after"])

        if txn_type in ("DEPOSIT", "RECEIVED"):
            cr_dr = "CREDIT"
        elif txn_type == "PIN_CHANGE":
            cr_dr = "—"
        else:
            cr_dr = "DEBIT"

        print(f"  {date_str:<12} {txn_type:<12} {amount:>14} "
              f"{cr_dr:<8} {bal:>14}")
