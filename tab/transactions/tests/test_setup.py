"""
Test setup file.
"""
import json
from rest_framework.test import APITestCase
from core.models import Account, Transaction
from transactions import views as tviews


# Functions to load data and help testcases
def create_account(**params):
    """Create and return a new account."""
    defaults = {"id": "7299be1b-8506-4702-8eb9-c418761f2dcf",
                "name": "TEST ACCOUNT 1"}
    defaults.update(params)
    return Account.objects.create(**defaults)


def get_account(id, name=None):
    account = None
    try:
        account = Account.objects.get(id=id)
    except Account.DoesNotExist:
        account = create_account(id=id, name=name)
    return account


def add_transaction(**params):
    """Create and return a sample transactions."""
    defaults = {
        "id": "T-01",
        "accountId": None,
        "amount": "1000000",
        "currency": "GBP",
        "type": "Settled",
        "dateTime": "2021-04-20T12:08:25+00:00",
    }
    defaults.update(params)
    transaction = Transaction.objects.create(**defaults)
    return transaction


# Create your tests here.
def get_data_from_file(filename, field, value):
    try:
        with open("static/" + filename) as data_file:
            json_data = json.load(data_file)
        data = [d for d in json_data if d[field] == value]
        return data
    except:
        return


def get_data(filename):
    with open("static/" + filename) as data_file:
        json_data = json.load(data_file)
        return json_data


class TestSetUp(APITestCase):
    def setUp(self):
        # load accounts to test db
        super(TestSetUp, self).setUp()
        self.account = []
        for a in get_data("accounts.json"):
            self.account.append(create_account(id=a["id"], name=a["name"]))

    def tearDown(self):
        return super(TestSetUp, self).tearDown()


class TestTransactionSetUp(TestSetUp):
    def setUp(self):
        # load accounts to test db
        super(TestTransactionSetUp, self).setUp()
        # load transactions to test db
        self.transactions = []
        for a in get_data("transactions.json"):
            account = get_account(id=a["accountId"])
            a["accountId"] = account
            self.transactions.append(add_transaction(**a))
        self.tsv = tviews.TransactionSummayView()
        self.trans = get_data_from_file(
            "transactions.json", "accountId", self.account[0].id
        )

    def tearDown(self):
        return super(TestTransactionSetUp, self).tearDown()
