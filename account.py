"""
account.py — Account creation and account details display.

Handles:
  • Interactive account creation with full validation
  • Displaying account details (masked sensitive data)

NOTE: EDUCATIONAL SIMULATION — NOT a real banking system.
"""

from config import (
    ACCOUNT_TYPES, INDIAN_STATES, SEPARATOR, THIN_SEP,
    MIN_OPENING_BALANCE, BRANCH_NAME
)
from validation import (
    validate_name, validate_mobile, validate_email,
    validate_dob, validate_pin, validate_address, validate_city
)
from database import create_customer_and_account
from utils import (
    print_banner, print_success, print_error, print_info,
    get_choice, press_enter, format_currency, mask_account_number,
    mask_mobile, format_date, generate_ifsc, print_menu
)


# ──────────────────────────────────────────────
# Account Creation (Interactive)
# ──────────────────────────────────────────────
def create_account():
    """
    Walk the user through creating a new bank account.
    Collects personal info, validates each field, and stores
    the new customer + account in the database.
    """
    print_banner("ACCOUNT REGISTRATION")
    print_info(f"Minimum opening balance: {format_currency(MIN_OPENING_BALANCE)}")
    print()

    # --- Full Name ---
    while True:
        name = get_choice("  Full Name          : ")
        ok, err = validate_name(name)
        if ok:
            break
        print_error(err)

    # --- Mobile Number ---
    while True:
        mobile = get_choice("  Mobile Number      : ")
        ok, err = validate_mobile(mobile)
        if ok:
            break
        print_error(err)

    # --- Email ---
    while True:
        email = get_choice("  Email Address      : ")
        ok, err = validate_email(email)
        if ok:
            break
        print_error(err)

    # --- Date of Birth ---
    while True:
        dob = get_choice("  Date of Birth (DD-MM-YYYY): ")
        ok, err = validate_dob(dob)
        if ok:
            break
        print_error(err)

    # --- Address ---
    while True:
        address = get_choice("  Address            : ")
        ok, err = validate_address(address)
        if ok:
            break
        print_error(err)

    # --- City ---
    while True:
        city = get_choice("  City               : ")
        ok, err = validate_city(city)
        if ok:
            break
        print_error(err)

    # --- State ---
    print("\n  Select State:")
    for i, s in enumerate(INDIAN_STATES, 1):
        print(f"    {i:2}. {s}")
    while True:
        state_choice = get_choice("  State number       : ")
        try:
            idx = int(state_choice)
            if 1 <= idx <= len(INDIAN_STATES):
                state = INDIAN_STATES[idx - 1]
                break
        except ValueError:
            pass
        print_error("Please enter a valid state number.")

    # --- Account Type ---
    print("\n  Account Type:")
    print_menu(list(ACCOUNT_TYPES.values()))
    while True:
        acc_type_choice = get_choice("  Select account type: ")
        if acc_type_choice in ACCOUNT_TYPES:
            account_type = ACCOUNT_TYPES[acc_type_choice]
            break
        print_error("Please select 1 or 2.")

    # --- PIN ---
    while True:
        pin = get_choice("  Set PIN (4 or 6 digits): ")
        ok, err = validate_pin(pin)
        if not ok:
            print_error(err)
            continue
        confirm = get_choice("  Confirm PIN        : ")
        if pin != confirm:
            print_error("PINs do not match. Try again.")
            continue
        break

    # --- Create the account ---
    try:
        customer_id, account_number = create_customer_and_account(
            name=name.strip().title(),
            mobile=mobile.strip(),
            email=email.strip().lower(),
            dob=dob.strip(),
            address=address.strip(),
            city=city.strip().title(),
            state=state,
            account_type=account_type,
            pin=pin
        )
    except Exception as e:
        print_error(f"Failed to create account: {e}")
        press_enter()
        return

    # --- Display success ---
    print(f"\n{SEPARATOR}")
    print("  ACCOUNT CREATED SUCCESSFULLY!".center(58))
    print(SEPARATOR)
    print(f"  Customer ID      : {customer_id}")
    print(f"  Account Number   : {account_number}")
    print(f"  Account Type     : {account_type}")
    print(f"  IFSC Code        : {generate_ifsc()}")
    print(f"  Branch           : {BRANCH_NAME}")
    print(f"  Opening Balance  : {format_currency(MIN_OPENING_BALANCE)}")
    print(THIN_SEP)
    print_info("Please note your Account Number and PIN securely.")
    print_info("You will need them to log in.")
    print(SEPARATOR)
    press_enter()


# ──────────────────────────────────────────────
# Display Account Details
# ──────────────────────────────────────────────
def display_account_details(info):
    """
    Print account details for a logged-in customer.
    Sensitive fields are masked.

    `info` is the merged customer+account dictionary
    returned by database.get_full_account_info().
    """
    print_banner("ACCOUNT DETAILS")
    print(f"  Customer Name    : {info['name']}")
    print(f"  Customer ID      : {info['customer_id']}")
    print(f"  Account Number   : {mask_account_number(info['account_number'])}")
    print(f"  Account Type     : {info['account_type']}")
    print(f"  Mobile Number    : {mask_mobile(info['mobile'])}")
    print(f"  Email            : {info['email']}")
    print(f"  Branch           : {info['branch']}")
    print(f"  IFSC Code        : {info['ifsc']}")
    print(f"  Account Status   : {info['status']}")
    print(f"  Opened On        : {format_date(info['created_at'])}")
    print(f"  Current Balance  : {format_currency(info['balance'])}")
    print(SEPARATOR)
    press_enter()
