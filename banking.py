import csv
from datetime import datetime

class Date:
    def __init__(self, csv_file):
        self.csv_file = csv_file

    def read_transactions(self):
        transactions = []
        with open(self.csv_file, mode='r') as file:
            reader = csv.DictReader(file)
            for row in reader:
                transactions.append(row)
        return transactions

    def write_transactions(self, transactions):
        with open(self.csv_file, mode='w', newline='') as file:
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

    def deposit(self, amount):
        if amount > 0:
            self.balance += amount
            print(f"Deposited {amount} into account {self.account_number}")
        else:
            print("Deposit amount must be positive.")

    def withdraw(self, amount):
        if amount > 0:
            if self.balance - amount < -100:
                print("Withdrawal would result in a balance lower than allowed (-100).")
            else:
                self.balance -= amount
                print(f"Withdrew {amount} from account {self.account_number}")
                if self.balance < 0:
                    self.balance -= 35  # Apply overdraft fee
                    self.overdrafts += 1
                    print("Overdraft fee of $35 applied.")
                    if self.overdrafts > 2:
                        print(f"Account {self.account_number} has been deactivated due to multiple overdrafts.")
                        self.balance = 0  # Deactivate account
        else:
            print("Withdrawal amount must be positive.")

    def transfer(self, target_account, amount):
        if self.balance >= amount:
            self.balance -= amount
            target_account.balance += amount
            print(f"Transferred {amount} from account {self.account_number} to account {target_account.account_number}")
        else:
            print("Insufficient funds for transfer.")

    def get_balance(self):
        print(f"Account Number: {self.account_number}, Balance: {self.balance}, Account Type: {self.account_type}")

    @classmethod
    def create_account(cls, account_number, account_type='Checking', initial_balance=0):
        if account_type not in ['Checking', 'Savings']:
            print("Invalid account type. Defaulting to Checking account.")
            account_type = 'Checking'
        return cls(account_number, initial_balance, account_type)

    def reactivate_account(self):
        if self.balance >= 0:
            self.overdrafts = 0
            print(f"Account {self.account_number} has been reactivated.")

    def save_transaction(self, transaction_type, amount, account_type):
        transaction = {
            'account_number': self.account_number,
            'transaction_type': transaction_type,
            'amount': amount,
            'balance': self.balance,
            'date': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        }
        
        with open(f'{account_type}_transactions.csv', mode='a', newline='') as file:
            fieldnames = ['account_number', 'transaction_type', 'amount', 'balance', 'date']
            writer = csv.DictWriter(file, fieldnames=fieldnames)
            if file.tell() == 0:  # Check if file is empty and write header
                writer.writeheader()
            writer.writerow(transaction)
            print(f"Transaction {transaction_type} of {amount} saved.")


class Customer:
    def __init__(self, account_id, first_name, last_name, password, balance_checking=0, balance_savings=0):
        self.account_id = account_id
        self.first_name = first_name
        self.last_name = last_name
        self.password = password
        self.checking_account = Account.create_account(account_id + "_checking", 'Checking', balance_checking)
        self.savings_account = Account.create_account(account_id + "_savings", 'Savings', balance_savings)

    def get_account_info(self):
        self.checking_account.get_balance()
        self.savings_account.get_balance()

    def deposit_to_checking(self, amount):
        self.checking_account.deposit(amount)

    def deposit_to_savings(self, amount):
        self.savings_account.deposit(amount)

    def withdraw_from_checking(self, amount):
        self.checking_account.withdraw(amount)

    def withdraw_from_savings(self, amount):
        self.savings_account.withdraw(amount)

    def transfer_between_accounts(self, amount):
        if self.checking_account.balance >= amount:
            self.checking_account.balance -= amount
            self.savings_account.balance += amount
            print(f"Transferred {amount} from checking to savings.")
        else:
            print(f"Insufficient funds in checking account.")


class Login:
    def __init__(self):
        self.customers = {}

    def add_customer(self, customer):
        self.customers[customer.account_id] = customer

    def login(self, account_id, password):
        if account_id in self.customers:
            customer = self.customers[account_id]
            if customer.password == password:
                print(f"Welcome back, {customer.first_name} {customer.last_name}!")
                return customer
            else:
                print("Incorrect password.")
        else:
            print("Account not found.")
        return None


if __name__ == "__main__":
    login_system = Login()
    
    customer1 = Customer('10001', 'Roqaya', 'Ali', 'password123', 1000 , 5000)
    customer2 = Customer('10002', 'Sara', 'Ali', 'password456', 3000, 10000)
    login_system.add_customer(customer1)
    login_system.add_customer(customer2)
    logged_in_customer = login_system.login('10001', 'password123')  # Login with correct credentials

    if logged_in_customer:
        logged_in_customer.deposit_to_checking(2000)
        logged_in_customer.get_account_info()

        logged_in_customer.withdraw_from_checking(1000)
        logged_in_customer.get_account_info()
        
        logged_in_customer.transfer_between_accounts(300)
        logged_in_customer.get_account_info()

        logged_in_customer.withdraw_from_checking(700)  # Overdraft
        logged_in_customer.get_account_info()
