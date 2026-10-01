# 🏦 Indian Banking System — Python Mini Project

> **EDUCATIONAL BANKING SIMULATION — NOT A REAL BANKING SYSTEM**
>
> This project does **not** connect to any real bank, UPI, NPCI, RBI system,
> Aadhaar, PAN database, or payment gateway. All data is stored locally in a
> SQLite database for learning purposes only.

---

## 📋 Project Description

A menu-driven, terminal-based banking application that simulates a simplified
Indian bank.  The system allows customers to create accounts, log in securely,
perform deposits, withdrawals, and transfers, view transaction history, and
change their PIN — all modelled around common Indian banking workflows.

An administrator dashboard provides account oversight, search, freeze/unfreeze
capabilities, and bank-wide statistics.

---

## 🎯 Objective

Combine core Python concepts into a single, real-world application that
demonstrates variables, data types, functions, OOP, file/database handling,
exception handling, modules, and standard-library usage — suitable for a
college mini-project or viva.

---

## ✨ Features

### Customer Features
| # | Feature | Description |
|---|---------|-------------|
| 1 | Create Account | Register with validated Indian personal info |
| 2 | Secure Login | Account number + hashed PIN with attempt locking |
| 3 | View Account Details | Masked display of account information |
| 4 | Check Balance | Indian Rupee formatted balance (₹1,23,456.00) |
| 5 | Deposit Money | With transaction ID and receipt |
| 6 | Withdraw Money | Minimum-balance enforcement |
| 7 | Transfer Money | Atomic IMPS/NEFT/UPI simulated transfers |
| 8 | Transaction History | Full tabular history |
| 9 | Mini Statement | Last 5 transactions at a glance |
| 10 | Change PIN | Verified old PIN → new PIN flow |

### Admin Features
| # | Feature | Description |
|---|---------|-------------|
| 1 | View All Accounts | Tabular list of every account |
| 2 | Search Account | By name, mobile, account no, or customer ID |
| 3 | View Account Details | Full unmasked details |
| 4 | Freeze / Unfreeze | Toggle account status |
| 5 | View Transactions | View any account's history |
| 6 | Bank Statistics | Aggregate deposits, withdrawals, transfers |

---

## 🛠 Technologies Used

| Technology | Purpose |
|-----------|---------|
| Python 3 | Core language |
| SQLite (`sqlite3`) | Persistent local database |
| `hashlib` | SHA-256 PIN hashing |
| `datetime` | Timestamps and date formatting |
| `random` | Account number / transaction ID generation |
| `uuid` | Customer ID generation |
| `os` | File paths, screen clearing |
| `re` | Input validation (regex) |
| `sys` | Application exit |

**No external packages required.**

---

## 📚 Python Concepts Demonstrated

- Variables and Data Types
- Input / Output
- Conditional Statements (`if` / `elif` / `else`)
- Loops (`while`, `for`)
- Functions (with parameters and return values)
- Lists and Dictionaries
- String Manipulation
- Modules and Imports
- File / Database Handling (SQLite)
- Exception Handling (`try` / `except`)
- Basic OOP (classes in `models.py`)
- Hashing (`hashlib`)
- Regular Expressions (`re`)
- Date/Time (`datetime`)
- Random Number Generation (`random`, `uuid`)

---

## 🇮🇳 Indian Banking Concepts Simulated

- Indian Rupee (₹) with Indian numbering (lakhs/crores grouping)
- Savings Account / Current Account
- IFSC Code and Branch Name
- 12-digit Account Number
- UPI / IMPS / NEFT transfer modes (simulated labels)
- 10-digit Indian Mobile Number validation
- 4-digit or 6-digit PIN
- Customer ID
- Transaction Reference / UTR Numbers
- Mini Statement
- Account Freeze / Lock mechanisms
- Minimum Balance requirements

---

## 📁 Project Structure

```
banking_system/
│
├── main.py              # Application entry point
├── config.py            # All configuration constants
├── database.py          # SQLite setup, queries, atomic transfers
├── models.py            # Data model classes (Customer, Account, Transaction)
├── authentication.py    # PIN hashing, verification, login flow
├── account.py           # Account creation and details display
├── transactions.py      # Deposit, withdraw, transfer, history, PIN change
├── admin.py             # Admin login and dashboard
├── validation.py        # Input validation (mobile, email, PIN, amount, …)
├── utils.py             # Currency formatting, ID generators, display helpers
│
├── data/
│   └── bank.db          # SQLite database (auto-created on first run)
│
├── README.md            # This file
├── requirements.txt     # Dependency info (standard library only)
└── .gitignore           # Git ignore rules
```

---

## 🚀 Installation & How to Run

### Prerequisites
- Python 3.7 or above

### Steps

```bash
# 1. Clone or download the project
git clone <repository-url>
cd banking_system

# 2. Run the application
python main.py
```

The database (`data/bank.db`) is **created automatically** on the first run.
Two demo accounts are seeded for immediate testing.

---

## 🔑 Default Credentials

### Admin Login
| Field | Value |
|-------|-------|
| Username | `admin` |
| Password | `admin1234` |

### Demo Customer Accounts (seeded on first run)

| Name | PIN | Balance |
|------|-----|---------|
| Rahul Kumar | 1234 | ₹25,000 |
| Priya Sharma | 5678 | ₹25,000 |

> Account numbers are generated randomly. Use **Admin → View All Accounts**
> to see them after starting the app.

---

## 📖 Sample Workflow (5–10 min demo)

1. **Start** → `python main.py`
2. **Create Account** → Fill in details → Note the generated account number
3. **Customer Login** → Enter account number + PIN
4. **Deposit** → ₹10,000
5. **Withdraw** → ₹2,000
6. **Transfer** → ₹1,500 to a demo account (IMPS mode)
7. **Transaction History** → View all transactions in a table
8. **Mini Statement** → Quick summary
9. **Change PIN** → Set a new PIN
10. **Logout** → Return to main menu
11. **Login again** → Verify new PIN works and balance persists
12. **Admin Login** → `admin` / `admin1234`
13. **View All Accounts** → See all customers
14. **Bank Statistics** → Aggregated data
15. **Exit** → Data saved in SQLite

---

## 🗄 Database Information

### Tables

#### `customers`
| Column | Type | Description |
|--------|------|-------------|
| customer_id | TEXT (PK) | Unique customer ID |
| name | TEXT | Full name |
| mobile | TEXT | 10-digit Indian mobile |
| email | TEXT | Email address |
| dob | TEXT | Date of birth |
| address | TEXT | Street address |
| city | TEXT | City |
| state | TEXT | State / UT |

#### `accounts`
| Column | Type | Description |
|--------|------|-------------|
| account_number | TEXT (PK) | 12-digit account number |
| customer_id | TEXT (FK) | Links to customers table |
| account_type | TEXT | Savings / Current |
| balance | REAL | Current balance in ₹ |
| pin_hash | TEXT | SHA-256 hash of PIN |
| ifsc | TEXT | IFSC code |
| branch | TEXT | Branch name |
| status | TEXT | ACTIVE / FROZEN / LOCKED / CLOSED |
| created_at | TEXT | Account creation timestamp |
| failed_attempts | INTEGER | Consecutive failed logins |

#### `transactions`
| Column | Type | Description |
|--------|------|-------------|
| transaction_id | TEXT (PK) | Unique transaction ID |
| account_number | TEXT (FK) | Account involved |
| transaction_type | TEXT | DEPOSIT / WITHDRAWAL / TRANSFER / RECEIVED / PIN_CHANGE |
| amount | REAL | Transaction amount |
| description | TEXT | Human-readable description |
| reference_number | TEXT | Reference / UTR number |
| transaction_date | TEXT | Timestamp |
| balance_after | REAL | Balance after this transaction |
| status | TEXT | SUCCESS / FAILED |

---

## ✅ Testing Checklist

| # | Test Case | Expected Result |
|---|-----------|----------------|
| 1 | Create valid account | Account created with unique number |
| 2 | Create account with invalid mobile | Error: must be 10-digit Indian number |
| 3 | Create account with mismatched PIN | Error: PINs do not match |
| 4 | Login with correct PIN | Dashboard displayed |
| 5 | Login with wrong PIN | Error with remaining attempts shown |
| 6 | Login after 3 failed attempts | Account locked message |
| 7 | Check balance | Balance displayed in ₹ format |
| 8 | Deposit valid amount | Balance increases, transaction recorded |
| 9 | Deposit invalid amount (negative/zero) | Error message |
| 10 | Withdraw valid amount | Balance decreases |
| 11 | Withdraw more than balance | Insufficient funds error |
| 12 | Transfer to valid account | Both balances updated |
| 13 | Transfer to invalid account | Account not found error |
| 14 | Transfer to own account | Self-transfer blocked |
| 15 | View transaction history | Table of all transactions |
| 16 | Change PIN | New PIN accepted |
| 17 | Login with new PIN | Successful login |
| 18 | Admin: Freeze account | Status changes to FROZEN |
| 19 | Login to frozen account | Access denied message |
| 20 | Admin: Unfreeze account | Status changes to ACTIVE |
| 21 | Logout | Returns to main menu |
| 22 | Exit application | Clean exit |
| 23 | Restart and verify persistence | All data intact |

---

## ⚠ Limitations

- **Not production-grade security** — SHA-256 without salt is used for
  educational simplicity. Real systems use bcrypt/scrypt/argon2.
- **Single-branch simulation** — All accounts share one branch and IFSC.
- **No real transactions** — UPI/IMPS/NEFT labels are simulated only.
- **Single-user terminal** — No concurrent multi-user support.
- **No encryption at rest** — SQLite database is unencrypted.
- **No network features** — Fully offline, local-only application.

---

## 🔮 Future Enhancements

- ATM simulation mode
- UPI QR code simulation
- Loan management system
- Fixed deposits & Recurring deposits
- Interest calculation
- Credit / Debit card simulation
- OTP simulation for transfers
- Email / SMS notification simulation
- PDF bank statement generation
- GUI using Tkinter
- Web interface using Flask / Django
- REST API backend
- Role-based authentication (multiple admin roles)
- Two-factor authentication
- Audit logging with timestamps
- Multi-branch support

---

## 📄 License

This project is created for **educational purposes only**.

---

## 🙏 Acknowledgements

Built as a Python mini project to demonstrate core programming concepts
within an Indian banking context.

> **Disclaimer:** This project is an educational simulation and does not
> connect to real banking or payment infrastructure. Do not use it for
> any real financial transactions.
