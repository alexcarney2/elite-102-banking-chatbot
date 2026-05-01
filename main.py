import sqlite3

# Connect to database
conn = sqlite3.connect("bank.db")
cursor = conn.cursor()

# Create table
cursor.execute("""
CREATE TABLE IF NOT EXISTS accounts (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT UNIQUE NOT NULL,
    password TEXT NOT NULL,
    full_name TEXT NOT NULL,
    balance REAL NOT NULL
)
""")
conn.commit()


def signup():
    print("Sign Up ")
    username = input("Create username: ")

    cursor.execute("SELECT * FROM accounts WHERE username = ?", (username,))
    if cursor.fetchone():
        print("Username already exists.")
        return

    password = input("Create password: ")
    full_name = input("Enter full name: ")

    cursor.execute(
        "INSERT INTO accounts (username, password, full_name, balance) VALUES (?, ?, ?, ?)",
        (username, password, full_name, 0.0)
    )
    conn.commit()

    print("Account created successfully!")


def login():
    print("Login")
    username = input("Username: ")
    password = input("Password: ")

    cursor.execute(
        "SELECT * FROM accounts WHERE username = ? AND password = ?",
        (username, password)
    )
    user = cursor.fetchone()

    if user:
        print(f"Welcome, {user[3]}!")
        banking_menu(username)
    else:
        print("Invalid username or password.")


def banking_menu(username):
    while True:
        cursor.execute("SELECT balance FROM accounts WHERE username = ?", (username,))
        balance = cursor.fetchone()[0]

        print("--- Main Menu ---")
        print(f"Balance: ${balance:.2f}")
        print("1. Deposit")
        print("2. Withdraw")
        print("3. Account Details")
        print("4. Logout")

        choice = input("Choose an option: ")

        if choice == "1":
            deposit(username)
        elif choice == "2":
            withdraw(username)
        elif choice == "3":
            account_details(username)
        elif choice == "4":
            print("Logging out...")
            break
        else:
            print("Invalid option.")


def deposit(username):
    try:
        amount = float(input("Enter deposit amount: $"))

        if amount <= 0:
            print("Amount must be greater than 0.")
            return

        cursor.execute(
            "UPDATE accounts SET balance = balance + ? WHERE username = ?",
            (amount, username)
        )
        conn.commit()

        print("Deposit successful.")
    except ValueError:
        print("Invalid input.")


def withdraw(username):
    try:
        amount = float(input("Enter withdrawal amount: $"))

        cursor.execute("SELECT balance FROM accounts WHERE username = ?", (username,))
        balance = cursor.fetchone()[0]

        if amount <= 0:
            print("Amount must be greater than 0.")
        elif amount > balance:
            print("Insufficient funds.")
        else:
            cursor.execute(
                "UPDATE accounts SET balance = balance - ? WHERE username = ?",
                (amount, username)
            )
            conn.commit()
            print("Withdrawal successful.")
    except ValueError:
        print("Invalid input.")


def account_details(username):
    cursor.execute(
        "SELECT id, full_name, balance FROM accounts WHERE username = ?",
        (username,)
    )
    user = cursor.fetchone()

    print("Account Details")
    print(f"Account ID: {user[0]}")
    print(f"Name: {user[1]}")
    print(f"Balance: ${user[2]:.2f}") #bring account balance with 2 decimal places


def main():
    while True:
        print("Banking App")
        print("1. Sign Up")
        print("2. Login")
        print("3. Exit")

        choice = input("Choose an option: ")

        if choice == "1":
            signup()
        elif choice == "2":
            login()
        elif choice == "3":
            print("Goodbye!")
            break
        else:
            print("Invalid option.")


main()
conn.close()