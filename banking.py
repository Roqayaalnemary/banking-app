import csv
from datetime import datetime

class Date:
    def __init__(self, bank_csv):
        self.bank_csv = bank_csv

    def read_transactions(self):
        transactions = []
        with open(self.bank_csv, mode='r') as file:
            reader = csv.DictReader(file)
            for row in reader:
                transactions.append(row)
        return transactions

    def write_transactions(self, transactions):
        with open(self.bank_csv, mode='w', newline='') as file:
            fieldnames = ['account_number', 'transaction_type', 'amount', 'balance', 'date']
            writer = csv.DictWriter(file, fieldnames=fieldnames)
            writer.writeheader()
            for transaction in transactions:
                writer.writerow(transaction)


class Account:
    def __init__(self, account_number, initial_balance=0, account_type='Checking'):
        self.account_number = account_number
        self.balance = initial_balance
        self.account_type = account_type
        self.overdrafts = 0
        self.deactivated = False

    def deposit(self, amount):
        if amount > 0:
            self.balance += amount
            self.save_transaction('Deposit', amount)
            print(f"Deposited ${amount} into account {self.account_number}")
        else:
            print("Deposit amount must be positive.")

    def withdraw(self, amount):
        if self.deactivated:
            print("Account is deactivated due to multiple overdrafts.")
            return
        
        if amount > 100:
            print("You cannot withdraw more than $100 per transaction.")
            return
        
        if amount > 0:
            if self.balance - amount < -100:
                print("Withdrawal denied! Account cannot go below -$100.")
            else:
                self.balance -= amount
                self.save_transaction('Withdrawal', amount)
                print(f"Withdrew ${amount} from account {self.account_number}")
                if self.balance < 0:
                    self.balance -= 35 
                    self.overdrafts += 1
                    print("⚠️ Overdraft fee of $35 applied.")
                    if self.overdrafts > 2:
                        self.deactivated = True
                        print(f"Account {self.account_number} has been deactivated due to multiple overdrafts.")
        else:
            print("Withdrawal amount must be positive.")

    def transfer(self, target_account, amount):
        if self.balance >= amount:
            self.balance -= amount
            target_account.balance += amount
            self.save_transaction('Transfer', amount)
            print(f"Transferred ${amount} from account {self.account_number} to account {target_account.account_number}")
        else:
            print("Insufficient funds for transfer.")

    def get_balance(self):
        print(f"Account Number: {self.account_number}, Balance: ${self.balance}, Account Type: {self.account_type}")

    def save_transaction(self, transaction_type, amount):
        transaction = {
            'account_number': self.account_number,
            'transaction_type': transaction_type,
            'amount': amount,
            'balance': self.balance,
            'date': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        }

        with open('bank.csv', mode='a', newline='') as file:
            fieldnames = ['account_number', 'transaction_type', 'amount', 'balance', 'date']
            writer = csv.DictWriter(file, fieldnames=fieldnames)
            if file.tell() == 0:
                writer.writeheader()
            writer.writerow(transaction)


class Customer:
    def __init__(self, account_id, first_name, last_name, password, balance_checking=0, balance_savings=0, accounts=None):
        self.account_id = account_id
        self.first_name = first_name
        self.last_name = last_name
        self.password = password
        self.accounts = accounts if accounts else []
        if 'Checking' in self.accounts:
            self.checking_account = Account(account_id + "_checking", balance_checking, 'Checking')
        if 'Savings' in self.accounts:
            self.savings_account = Account(account_id + "_savings", balance_savings, 'Savings')

    def get_account_info(self):
        if hasattr(self, 'checking_account'):
            self.checking_account.get_balance()
        if hasattr(self, 'savings_account'):
            self.savings_account.get_balance()

    def deposit_to_checking(self, amount):
        if hasattr(self, 'checking_account'):
            self.checking_account.deposit(amount)

    def deposit_to_savings(self, amount):
        if hasattr(self, 'savings_account'):
            self.savings_account.deposit(amount)

    def withdraw_from_checking(self, amount):
        if hasattr(self, 'checking_account'):
            self.checking_account.withdraw(amount)

    def withdraw_from_savings(self, amount):
        if hasattr(self, 'savings_account'):
            self.savings_account.withdraw(amount)

    def transfer_between_accounts(self, amount):
        if hasattr(self, 'checking_account') and hasattr(self, 'savings_account'):
            if self.checking_account.balance >= amount:
                self.checking_account.balance -= amount
                self.savings_account.balance += amount
                print(f"Transferred ${amount} from Checking to Savings.")
            else:
                print("Insufficient funds in Checking.")
        else:
            print("One or both accounts do not exist.")

    def transfer_to_other_customer(self, other_customer, amount):
        if hasattr(self, 'checking_account') and self.checking_account.balance >= amount:
            self.checking_account.balance -= amount
            other_customer.checking_account.balance += amount
            print(f"Transferred ${amount} from your account to {other_customer.first_name} {other_customer.last_name}.")
        else:
            print("Insufficient funds.")


class Login:
    def __init__(self):
        self.customers = {}
        self.load_customers()

    def load_customers(self):
        try:
            with open('bank.csv', mode='r') as file:
                reader = csv.reader(file, delimiter=';')
                next(reader)  # Skip header row
                for row in reader:
                    account_id = row[0]
                    first_name = row[1]
                    last_name = row[2]
                    password = row[3]
                    balance_checking, balance_savings = map(float, row[4].split(','))
                    accounts = []
                    if balance_checking > 0:
                        accounts.append('Checking')
                    if balance_savings > 0:
                        accounts.append('Savings')
                    customer = Customer(account_id, first_name, last_name, password, balance_checking, balance_savings, accounts)
                    self.customers[account_id] = customer
        except FileNotFoundError:
            print("No existing customers found. Starting fresh.")

    def add_customer(self, customer):
        self.customers[customer.account_id] = customer

    def login(self, account_id, password):
        if account_id in self.customers:
            customer = self.customers[account_id]
            if customer.password == password:
                print(f"🔓 Welcome back, {customer.first_name} {customer.last_name}!")
                return customer
            else:
                print("Incorrect password.")
        else:
            print("Account not found.")
        return None


def add_new_customer(login_system, filename='bank.csv'):
    print("\nCreate a New Bank Account")
    account_id = input("Enter Account ID: ")
    first_name = input("Enter First Name: ")
    last_name = input("Enter Last Name: ")
    password = input("Set a Password: ")

    balance_checking = float(input("Initial Deposit for Checking: "))
    balance_savings = float(input("Initial Deposit for Savings: "))
    
    account_type = input("Choose Account Type (Checking, Savings, or Both): ").strip().lower()

    accounts = []
    if account_type in ['checking', 'both']:
        accounts.append('Checking')
    if account_type in ['savings', 'both']:
        accounts.append('Savings')

    new_customer = Customer(account_id, first_name, last_name, password, balance_checking, balance_savings, accounts)
    login_system.add_customer(new_customer)

    with open(filename, mode='a', newline='') as file:
        writer = csv.writer(file, delimiter=';')
        writer.writerow([account_id, first_name, last_name, password, f"{balance_checking},{balance_savings}"])

    print("New account created successfully!")


def user_interaction():
    login_system = Login()

    print("Welcome to the Banking System!")

    while True:
        print("\nSelect an option:")
        print("1️ Login")
        print("2️ Create New Account")
        print("3️ Exit")

        choice = input("Enter choice: ")

        if choice == '1':
            account_id = input("Enter Account ID: ")
            password = input("Enter Password: ")
            logged_in_customer = login_system.login(account_id, password)

            if logged_in_customer:
                while True:
                    print("\nChoose an option:")
                    print("1️ Deposit to Checking")
                    print("2️ Withdraw from Checking")
                    print("3️ Transfer from Checking to Savings")
                    print("4️ Withdraw from Savings")
                    print("5️ View Account Info")
                    print("6️ Logout")

                    sub_choice = input("Enter choice: ")

                    if sub_choice == '1':
                        amount = float(input("Enter deposit amount: "))
                        logged_in_customer.deposit_to_checking(amount)
                    elif sub_choice == '2':
                        amount = float(input("Enter withdrawal amount: "))
                        logged_in_customer.withdraw_from_checking(amount)
                    elif sub_choice == '3':
                        amount = float(input("Enter transfer amount: "))
                        logged_in_customer.transfer_between_accounts(amount)
                    elif sub_choice == '4':
                        amount = float(input("Enter withdrawal amount: "))
                        logged_in_customer.withdraw_from_savings(amount)
                    elif sub_choice == '5':
                        logged_in_customer.get_account_info()
                    elif sub_choice == '6':
                        print("Logged out successfully!")
                        break

        elif choice == '2':
            add_new_customer(login_system, 'bank.csv')
        elif choice == '3':
            print("Goodbye!")
            break


if __name__ == "__main__":
    user_interaction()
