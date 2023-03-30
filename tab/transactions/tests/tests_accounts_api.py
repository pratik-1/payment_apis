"""
Tests for accounts and transactions
"""
from django.urls import reverse
from rest_framework import status
from transactions import serializer as tserializers

from core.models import Account, Transaction
from .test_setup import TestSetUp, TestTransactionSetUp
from django.core import exceptions

ACCOUNT_URL = reverse("transactions:account-list")
TRANSACTION_URL = reverse("transactions:transaction-list")


def detail_url(account_id):
    """Return transaction detail URL."""
    return reverse("transactions:transaction-summary", args=[account_id])


# Write Tests here.
class AccountApiTests(TestSetUp):
    """Test account API requests."""

    def test_retrieve_accounts(self):
        """Test retrieving a list of accounts."""
        accounts = Account.objects.all().order_by("id")
        # get response for list of accounts
        res = self.client.get(ACCOUNT_URL)
        serializer = tserializers.AccountSerializer(accounts, many=True)
        # validate response
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)


class TransactionApiTests(TestTransactionSetUp):
    """Test Transaction API requests."""

    def test_retrieve_transactions(self):
        """Test retrieving a list of transactions."""
        # get handle for all created transactions
        transactions = Transaction.objects.all().order_by("id")

        # get response for list of transactions
        res = self.client.get(TRANSACTION_URL)

        serializer = tserializers.TransactionSerializer(transactions, many=True)
        # assert
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_update_transactions(self):
        """Test to update existing transaction."""
        # TODO: Write test


class TransactionSummayView(TestTransactionSetUp):
    def test_get_account_object(self):
        """Test if correct object is returned"""
        account = self.tsv.get_account_object(self.account[0].id)
        self.assertEqual(str(account), str(self.account[0]))

    def test_get_account_object_error(self):
        """Test when incorrect id is passed"""
        with self.assertRaises(exceptions.ValidationError):
            account = self.tsv.get_account_object("TEST")

    def test_get_transactions_list(self):
        """Test if transaction list is returned"""
        transactions = self.tsv.get_transactions_list(
            account_id=self.account[0].id)
        self.assertEqual(len(transactions), len(self.trans))
        self.assertEqual(transactions[0].id, self.transactions[0].id)

    def test_get_transaction_balance(self):
        """Test if the transaction and balance is correct"""
        # NOTE: Test fails due to incorrect calculation logic
        # TODO: Change the calculation logic
        transactions, balance = self.tsv.get_transaction_balance(
            self.account[0].id)
        self.assertEqual(transactions["chargeback"], {"GBP": 100300})
        self.assertEqual(balance, {"EUR": 139970, "GBP": 798700})

    def test_get_transaction_summary(self):
        """Test get request api for transaction summary with valid api format"""
        # check if request for test account is successful
        url = detail_url(self.account[0].id)
        res = self.client.get(url)
        self.assertEqual(res.status_code, status.HTTP_200_OK)

        # check if the response returned is in valid format with correct values
        expected = {
            "account": {
                "name": "TEST ACCOUNT 1",
                "id": "7299be1b-8506-4702-8eb9-c418761f2dcf",
            },
            "transactions": {
                "chargeback": {"GBP": 3000000},
                "refunded": {"GBP": 5000000},
                "settled": {"GBP": 21000000, "EUR": 1000000},
            },
            "balance": {"GBP": 29000000, "EUR": 1000000},
        }

        # check if the response returned is in valid format
        serializer = tserializers.TransactionBalanceSerializer(expected)
        self.assertEqual(res.data["account"], serializer.data["account"])
        self.assertEqual(res.data["transactions"],
                         serializer.data["transactions"])
        self.assertEqual(res.data["balance"], serializer.data["balance"])
