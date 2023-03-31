# Project Instructions

## Project setup

**Prerequisites**:

Your machine needs to have below pre-requisites installed:

- Git

**To get started follow the steps:**

1. Enter the below command in your shell to clone the repository

```commandline
git clone git@github.com:pratik-1/payment_apis.git
```

2. Navigate into the `payment_apis` folder.

3. Create virtual environment and activate

```commandline
python -m venv venv
venv\Scripts\activate
```

4. Install the dependencies

```commandline
pip install -r requirements.txt
```

5. Navigate to the `tab` folder.

## Run application Tests

Run application tests with below command. This will also test project is properly setup.

```commandline
python manage.py test
```

You will see one test fails with assertion error rest all are passed.

## Load database

To load database follow the steps:

1. Create a database. For this project default `sqlite.db` is configured.

```commandline
python manage.py migrate
```

2. Once the command is executed, you should see `db.sqlite3` create above manage.py file inside `tab` folder.

3. Load the database with sample data (accounts.json, transactions.json) present in `tab/static` folder.
   Run the below command to populate database.

```commandline
python manage.py runscript load_db
```

4. If no errors found then database should be populated.

5. To access to all the API endpoints. Run the command

```commandline
python manage.py runserver
```

6. Go to your browser and enter

```commandline
http://127.0.0.1:8000/api/docs/
```

![Payments APIs](https://user-images.githubusercontent.com/37976329/228940448-84108d3e-00dd-44b5-8960-615cf6db91d6.jpg)

**If you reach here and able to see all the endpoints this ensures project is setup with database intialized.**

## Explore APIs

To find the transaction summary of an account.

1. Select following api:

   `GET /transactions/{account_id}/balance`

2. Click 'Try it out' button. In `account_id` provide account id (for example: '3c37d5f7-9668-4195-a801-c87e0c79ba74')
3. Select 'Execute'. You should see status code 200 with response body as

```
{
  "account": {
      "id": "3c37d5f7-9668-4195-a801-c87e0c79ba74",
      "name": "TEST ACCOUNT 3"
  },
  "transactions": {
      "chargeback": {
          "EUR": 1300000,
          "GBP": 2000000
      },
      "refunded": {
          "GBP": 5020000
      },
      "settled": {
          "EUR": 2100000,
          "GBP": 21260000
      }
  },
  "balance": {
      "EUR": 3400000,
      "GBP": 28280000
  }
}
```

![Screenshot 2023-03-30 193917](https://user-images.githubusercontent.com/37976329/228937520-1590a8d8-f059-413e-b281-2ff9db457fff.jpg)

4. If you provide valid account id format but account is not present in database. You will see an error.

```
{
 "res": "Account id 8299be1b-8506-4702-8eb9-c418761f2dcf does not exists"
}
```

5. If the account id format is not valid. You will get validation error and need to provide correct format of account id.

**Feel free to create new account, add transactions for the account. Update and delete the accounts, transactions data.**
