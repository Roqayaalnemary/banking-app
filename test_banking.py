import unittest
import csv
from banking import Account, Customer, Login, Date
from unittest.mock import patch
from banking import CheckingAccount  

class TestAccount(unittest.TestCase):

    def setUp(self):
       
        self.account = Account(account_number="12345", initial_balance=100)

    def test_deposit(self):
    
        self.account.deposit(50)
        self.assertEqual(self.account.balance, 150)

    def test_withdraw(self):
        self.account.withdraw(50)
        self.assertEqual(self.account.balance, 50)

    def test_withdraw_more_than_balance(self):
        self.account.withdraw(150)
        self.assertEqual(self.account.balance, 100)

    def test_overdraft_fee(self):
      
        self.account.withdraw(120)
        self.assertEqual(self.account.balance, -70)  

    def test_transfer(self):
        
        target_account = Account(account_number="67890", initial_balance=50)
        self.account.transfer(target_account, 50)
        self.assertEqual(self.account.balance, 50)
        self.assertEqual(target_account.balance, 100)



class TestCustomer(unittest.TestCase):

    def setUp(self):
   
        self.customer = Customer(account_id="12345", first_name="John", last_name="Doe", password="password", balance_checking=100)

    def test_deposit_to_checking(self):
      
        self.customer.deposit_to_checking(50)
        self.assertEqual(self.customer.checking_account.balance, 150)

    def test_withdraw_from_checking(self):
    
        self.customer.withdraw_from_checking(50)
        self.assertEqual(self.customer.checking_account.balance, 50)

    def test_transfer_between_accounts(self):
   
        self.customer.transfer_between_accounts(50)
        self.assertEqual(self.customer.checking_account.balance, 50)
        self.assertEqual(self.customer.savings_account.balance, 50)



class TestLogin(unittest.TestCase):

    def setUp(self):
       
        self.login_system = Login()
        self.customer = Customer(account_id="12345", first_name="John", last_name="Doe", password="password")
        self.login_system.add_customer(self.customer)

    def test_login_success(self):
       
        customer = self.login_system.login("12345", "password")
        self.assertIsNotNone(customer)
        self.assertEqual(customer.first_name, "John")

    def test_login_fail(self):
       
        customer = self.login_system.login("12345", "wrongpassword")
        self.assertIsNone(customer)



class TestDate(unittest.TestCase):

    def setUp(self):
    
        self.date = Date(bank_csv='test_bank.csv')

    def test_read_transactions(self):
     
        with open('test_bank.csv', mode='w', newline='') as file:
            writer = csv.writer(file, delimiter=';')
            writer.writerow(['account_number', 'transaction_type', 'amount', 'balance'])
            writer.writerow(['12345', 'deposit', '100', '200'])
            writer.writerow(['67890', 'withdraw', '50', '150'])

        transactions = self.date.read_transactions()
        self.assertGreater(len(transactions), 0)

    def test_write_transactions(self):
    
        transactions = [
            {'account_number': '12345', 'transaction_type': 'deposit', 'amount': '100', 'balance': '200'},
            {'account_number': '67890', 'transaction_type': 'withdraw', 'amount': '50', 'balance': '150'}
        ]
        self.date.write_transactions(transactions)
      
        with open('test_bank.csv', 'r') as file:
            content = file.read()
            self.assertIn('12345', content)
            self.assertIn('67890', content)


if __name__ == '__main__':
    unittest.main()
