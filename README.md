# banking-app

## Description:
This is a simple banking system where users can create accounts, deposit money, withdraw funds, and transfer money between accounts. It also includes features such as overdraft protection.

## Features:
- Add new customer
- Create checking and savings accounts
- Withdraw from checking or savings
- Deposit into checking or savings
- Transfer between accounts
- Overdraft protection with $35 fee
- Prevent withdrawal of more than $100 when the balance is negative
- Account deactivation after 2 overdrafts

## Technologies Used:
- Python
- CSV file handling

## Challenges:
- Implementing overdraft protection:
  - This involved ensuring that the account cannot go below -$100 and applying an overdraft fee.
- Handling multiple accounts and transactions efficiently:
  - I had to ensure that both checking and savings accounts are handled correctly in terms of deposits, withdrawals, and transfers.
## Contributing:
1. Fork the repository.
2. Create a new branch (`git checkout -b feature-name`).
3. Make your changes and commit them (`git commit -am 'Add new feature'`).
4. Push to the branch (`git push origin feature-name`).
5. Create a new Pull Request.

## How to Run the Application:
1. Clone the repository to your local machine.
2. Make sure you have Python installed.
3. Run the `banking.py` script to start the banking system.

## Setup Instructions:
1. Ensure Python 3.6 or higher is installed.
2. Install any required dependencies (if applicable).
3. Run the script `banking.py` to use the banking app.

## Icebox Features:
- Implementing email notifications for account activities.
- Adding an admin interface for managing customers and transactions.
- Implementing a mobile version of the application.
