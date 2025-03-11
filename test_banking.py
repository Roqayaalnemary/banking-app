import unittest
from datetime import datetime
from banking import Account, Customer, Login, add_new_customer

class TestBankingSystem(unittest.TestCase):

    def setUp(self):
        """Setup before each test."""
        self.login_system = Login()  # Creating a Login instance
        # Create two customers for testing
        self.customer1 = Customer('user1', 'John', 'Doe', 'password123', 500, 100)
        self.customer2 = Customer('user2', 'Jane', 'Smith', 'password456', 200, 300)
        self.login_system.add_customer(self.customer1)
        self.login_system.add_customer(self.customer2)

    def test_create_new_account(self):
        """Test account creation functionality"""
        new_customer = Customer('user3', 'Alice', 'Brown', 'password789', 0, 500)
        self.login_system.add_customer(new_customer)
        
        # Verify if the new customer is added
        self.assertIn('user3', self.login_system.customers)

    def test_login_valid(self):
        """Test login with valid credentials"""
        logged_in_customer = self.login_system.login('user1', 'password123')
        self.assertEqual(logged_in_customer.first_name, 'John')
        self.assertEqual(logged_in_customer.last_name, 'Doe')

    def test_login_invalid(self):
        """Test login with invalid credentials"""
        logged_in_customer = self.login_system.login('user1', 'wrongpassword')
        self.assertIsNone(logged_in_customer)

    def test_deposit(self):
        """Test deposit functionality"""
        self.customer1.deposit_to_checking(200)
        self.assertEqual(self.customer1.checking_account.balance, 700)

    def test_withdraw(self):
        """Test withdrawal functionality"""
        self.customer1.withdraw_from_checking(100)
        self.assertEqual(self.customer1.checking_account.balance, 600)

    def test_withdraw_limit(self):
        """Test that withdrawal is limited to $100"""
        self.customer1.withdraw_from_checking(150)  # Exceeds the $100 limit
        self.assertEqual(self.customer1.checking_account.balance, 600)

    def test_overdraft_fee(self):
        """Test overdraft fee application"""
        self.customer1.withdraw_from_checking(700)  # Should go below $0 and trigger overdraft fee
        self.assertEqual(self.customer1.checking_account.balance, 600 - 700 - 35)

    def test_account_deactivation(self):
        """Test account deactivation after multiple overdrafts"""
        self.customer1.withdraw_from_checking(700)  # First overdraft
        self.customer1.withdraw_from_checking(700)  # Second overdraft
        self.customer1.withdraw_from_checking(700)  # Third overdraft, should deactivate
        self.assertTrue(self.customer1.checking_account.deactivated)

    def test_transfer_between_accounts(self):
        """Test transferring between accounts of the same customer"""
        self.customer1.transfer_between_accounts(100)
        self.assertEqual(self.customer1.checking_account.balance, 500)
        self.assertEqual(self.customer1.savings_account.balance, 200)

    def test_transfer_to_other_customer(self):
        """Test transferring money from one customer to another"""
        self.customer1.transfer_to_other_customer(self.customer2, 100)
        self.assertEqual(self.customer1.checking_account.balance, 400)
        self.assertEqual(self.customer2.checking_account.balance, 300 + 100)

    def test_view_account_info(self):
        """Test viewing account balance info"""
        # Capture the output of account info view
        self.customer1.get_account_info()

    def test_add_transaction_to_csv(self):
        """Test if a transaction is correctly added to the CSV file"""
        # Ensure a transaction is added when performing a deposit
        initial_count = sum(1 for _ in open('bank.csv'))
        self.customer1.deposit_to_checking(100)
        final_count = sum(1 for _ in open('bank.csv'))
        self.assertGreater(final_count, initial_count)

if __name__ == "__main__":
    unittest.main()
