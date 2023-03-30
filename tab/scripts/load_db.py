"""
Script to populate database with given json files.
"""
from core.models import Account, Transaction
import json

# Functions to load data
def create_account(**params):
    """Create and return a new account."""
    return Account.objects.create(**params)

def get_account(id):
    """Get account with input id."""
    return Account.objects.get(id=id)

def add_transaction(**params):
    """Create transactions."""
    return Transaction.objects.create(**params)

def get_data(filename):
    with open("static/" + filename) as data_file:
        json_data = json.load(data_file)
        return json_data

def run():
    Account.objects.all().delete()
    Transaction.objects.all().delete()
    for a in get_data("accounts.json"):
            create_account(id=a["id"], name=a["name"])

    for a in get_data("transactions.json"):
        account = get_account(id=a["accountId"])
        a["accountId"] = account
        add_transaction(**a)