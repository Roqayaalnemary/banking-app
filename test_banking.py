import unittest
from banking import Customer, Login, Account, Date
from datetime import datetime

class TestBankingApp(unittest.TestCase):
    
    def setUp(self):
        self.customer = Customer(account_id="10001", first_name="Roqaya", last_name="Ali", password="password123", balance_checking=500, balance_savings=1000)
        self.login_system = Login()
        self.login_system.add_customer(self.customer)

    def test_deposit(self):
        self.customer.deposit_to_checking(200)
        self.assertEqual(self.customer.checking_account.balance, 700)
        self.customer.deposit_to_savings(100)
        self.assertEqual(self.customer.savings_account.balance, 1100)

    def test_withdraw(self):
        self.customer.withdraw_from_checking(100)
        self.assertEqual(self.customer.checking_account.balance, 600)
        
        self.customer.withdraw_from_checking(700)  # Overdraft fee
        self.assertEqual(self.customer.checking_account.balance, -35)  # Account balance with fee

    def test_transfer_between_accounts(self):
        self.customer.transfer_between_accounts(100)
        self.assertEqual(self.customer.checking_account.balance, 500)
        self.assertEqual(self.customer.savings_account.balance, 1200)

    def test_deactivate_account_after_overdrafts(self):
        self.customer.withdraw_from_checking(700)  # Overdraft
        self.customer.withdraw_from_checking(100)  # Overdraft fee
        self.assertEqual(self.customer.checking_account.balance, 0)  # Account deactivated

    def test_reactivate_account_after_payment(self):
        self.customer.checking_account.reactivate_account()  # Reactivate the account
        self.assertEqual(self.customer.checking_account.balance, 0)  # Account reactivated

    def test_login(self):
        customer_logged_in = self.login_system.login("10001", "password123")
        self.assertEqual(customer_logged_in.first_name, "Roqaya")
        self.assertEqual(customer_logged_in.last_name, "Ali")
        
        customer_logged_in_failed = self.login_system.login("1001", "password123")
        self.assertIsNone(customer_logged_in_failed)

    def test_write_transactions_to_csv(self):
        transactions = [
            {'account_number': '123_checking', 'transaction_type': 'deposit', 'amount': 200, 'balance': 700, 'date': datetime.now().strftime('%Y-%m-%d %H:%M:%S')},
            {'account_number': '123_savings', 'transaction_type': 'deposit', 'amount': 100, 'balance': 1100, 'date': datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
        ]
        self.customer.checking_account.save_transaction('deposit', 200, 'Checking')
        self.customer.savings_account.save_transaction('deposit', 100, 'Savings')

    def tearDown(self):
        pass

if __name__ == "__main__":
    unittest.main()
    