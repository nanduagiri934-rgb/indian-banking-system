"""
main.py — Entry point for the Indian Banking System.

Run this file to start the application:
    python main.py

This is the main controller that:
  1. Initialises the database and seeds sample data
  2. Shows the main menu
  3. Routes to account creation, customer login, or admin login
  4. Runs the customer dashboard after successful login

==========================================================
  EDUCATIONAL BANKING SIMULATION — NOT A REAL BANKING SYSTEM
  This project is created for academic / learning purposes.
  It does NOT connect to any real bank, UPI, NPCI, or RBI
  system.  All data is stored locally in a SQLite database.
==========================================================
"""

import sys

# Ensure Unicode characters (like ₹) display correctly on Windows
if sys.stdout.encoding != "utf-8":
    sys.stdout.reconfigure(encoding="utf-8")
if sys.stdin.encoding != "utf-8":
    sys.stdin.reconfigure(encoding="utf-8")

from config import SEPARATOR, BANK_NAME
from database import initialize_database, seed_sample_data, get_full_account_info
from authentication import attempt_login
from account import create_account, display_account_details
from transactions import (
    check_balance, deposit, withdraw, transfer,
    transaction_history, mini_statement, change_pin
)
from admin import admin_login, admin_dashboard
from utils import (
    print_banner, print_success, print_error, print_info,
    get_choice, press_enter, clear_screen, print_menu
)


# ──────────────────────────────────────────────
# Customer Dashboard
# ──────────────────────────────────────────────
def customer_dashboard(info):
    """
    Menu loop for a logged-in customer.
    `info` is the merged customer+account dict from the DB.
    """
    while True:
        print_banner("CUSTOMER DASHBOARD")
        print(f"  Welcome, {info['name']}!")
        print_menu([
            "View Account Details",
            "Check Balance",
            "Deposit Money",
            "Withdraw Money",
            "Transfer Money",
            "Transaction History",
            "Mini Statement",
            "Change PIN",
            "Logout"
        ])

        choice = get_choice("  Enter your choice: ")

        if choice == "1":
            # Refresh info from DB before displaying
            info = get_full_account_info(info["account_number"]) or info
            display_account_details(info)
        elif choice == "2":
            check_balance(info)
        elif choice == "3":
            deposit(info)
        elif choice == "4":
            withdraw(info)
        elif choice == "5":
            transfer(info)
        elif choice == "6":
            transaction_history(info)
        elif choice == "7":
            mini_statement(info)
        elif choice == "8":
            change_pin(info)
        elif choice == "9":
            print_success("Logged out successfully.")
            press_enter()
            break
        else:
            print_error("Invalid choice. Please try again.")
            press_enter()


# ──────────────────────────────────────────────
# Customer Login
# ──────────────────────────────────────────────
def customer_login():
    """
    Prompt for account number and PIN, then hand off
    to the customer dashboard on success.
    """
    print_banner("CUSTOMER LOGIN")
    acc_no = get_choice("  Account Number : ")
    pin = get_choice("  PIN            : ")

    success, message, info = attempt_login(acc_no, pin)

    if success:
        print_success(message)
        press_enter()
        customer_dashboard(info)
    else:
        print_error(message)
        press_enter()


# ──────────────────────────────────────────────
# Main Menu
# ──────────────────────────────────────────────
def main():
    """
    Application entry point.
    Initialises the database, seeds demo data, and runs the
    main menu loop.
    """
    # --- Database setup ---
    initialize_database()
    seed_sample_data()

    # --- Main loop ---
    while True:
        print_banner()
        print_menu([
            "Create Account",
            "Customer Login",
            "Admin Login",
            "Exit"
        ])

        choice = get_choice("  Enter your choice: ")

        if choice == "1":
            create_account()
        elif choice == "2":
            customer_login()
        elif choice == "3":
            if admin_login():
                admin_dashboard()
        elif choice == "4":
            print(f"\n{SEPARATOR}")
            print("  Thank you for banking with us!".center(58))
            print(f"  {BANK_NAME}".center(58))
            print(SEPARATOR)
            sys.exit(0)
        else:
            print_error("Invalid choice. Please try again.")
            press_enter()


# ──────────────────────────────────────────────
# Run
# ──────────────────────────────────────────────
if __name__ == "__main__":
    main()
