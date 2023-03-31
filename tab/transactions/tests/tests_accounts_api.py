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


def detail_account_url(account_id):
    """Return transaction detail URL."""
    return reverse("transactions:account-detail", args=[account_id])

def detail_transaction_url(id):
    """Return transaction detail URL."""
    return reverse("transactions:transaction-detail", args=[id])

def detail_trx_summary_url(account_id):
    """Return transaction detail URL."""
    return reverse("transactions:transaction-summary", args=[account_id])


# Write Tests here.
class AccountApiTests(TestSetUp):
    """Test account API requests."""

    def test_retrieve_accounts(self):
        """Test retrieving a list of accounts."""
        accounts = Account.objects.all().order_by("name")
        # get response for list of accounts
        res = self.client.get(ACCOUNT_URL)
        serializer = tserializers.AccountSerializer(accounts, many=True)
        # validate response
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_update_account(self):
        """Test to update existing account."""
        # TODO: Write test
        payload = {"name": "NEW TEST ACCOUNT 1"}
        url = detail_account_url(self.account[0].id)

        # PATCH for partial update
        res = self.client.patch(url, payload)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.account[0].refresh_from_db()
        # check payload data is modified
        self.assertEqual(self.account[0].name, payload["name"])


    def test_delete_account(self):
        """Test to delete existing account."""
        url = detail_account_url(self.account[0].id)
        res = self.client.delete(url)

        # 204 standard http response to delete
        self.assertEqual(res.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Account.objects.filter(id=self.account[0].id).exists())


class TransactionApiTests(TestTransactionSetUp):
    """Test Transaction API requests."""

    def test_retrieve_transactions(self):
        """Test retrieving a list of transactions."""
        # get handle for all created transactions
        transactions = Transaction.objects.all().order_by("id")

        # get response for list of transactions
        res = self.client.get(TRANSACTION_URL)

        ser = tserializers.TransactionSerializer(transactions, many=True)
        # assert
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, ser.data)

    def test_update_transactions(self):
        """Test to update existing transaction."""
        # TODO: Write test
        payload = {"amount": "2000000", "currency": "EUR",}
        url = detail_transaction_url(self.transactions[0].id)

        # PATCH for partial update
        res = self.client.patch(url, payload)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.transactions[0].refresh_from_db()
        # check payload data is modified
        self.assertEqual(self.transactions[0].amount, int(payload["amount"]))
        self.assertEqual(self.transactions[0].currency, payload["currency"])

    def test_delete_transactions(self):
        """Test to delete existing transaction."""
        url = detail_transaction_url(self.transactions[0].id)
        res = self.client.delete(url)

        # 204 standard http response to delete
        self.assertEqual(res.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Transaction.objects.filter(
            id=self.transactions[0].id).exists())

class TransactionSummayView(TestTransactionSetUp):
    def test_get_object(self):
        """Test if correct object is returned"""
        account = self.tsv.get_object(model=Account,id=self.account[0].id)
        self.assertEqual(str(account), str(self.account[0]))

    def test_get_object_error(self):
        """Test when incorrect id format is passed"""
        with self.assertRaises(exceptions.ValidationError):
            _ = self.tsv.get_object(model=Account,id="TEST")

    def test_get_object_error(self):
        """Test when proper error raised if object does not exists"""
        with self.assertRaises(Account.DoesNotExist):
            _ = self.tsv.get_object(model=Account,
                                    id="7299be1b-8506-4702-8eb9-c418761f2ddf")


    def test_get_transactions_list(self):
        """Test if transaction list is returned"""
        transactions = self.tsv.get_transactions_list(model=Transaction,
                                                accountId=self.account[0].id)
        self.assertEqual(len(transactions), len(self.trans))
        self.assertEqual(transactions[0].id, self.transactions[0].id)


    def test_get_transactions_list_error(self):
        """Test if transaction list raises error when account does not exist"""
        with self.assertRaises(Account.DoesNotExist):
            _ = self.tsv.get_transactions_list(model=Transaction,
                            accountId="7299be1b-8506-4702-8eb9-c418761f2ddf")

    def test_get_transaction_balance(self):
        """Test if the transaction and balance is correct"""
        # NOTE: Test fails due to incorrect calculation logic
        # TODO: Change the calculation logic
        transactions, balance = self.tsv.get_transaction_balance(
            self.account[0].id)
        self.assertEqual(transactions["chargeback"], {"GBP": 100300})
        self.assertEqual(balance, {"EUR": 139970, "GBP": 798700})

    def test_get_transaction_summary(self):
        """Test get request api for transaction summary with valid format"""
        # check if request for test account is successful
        url = detail_trx_summary_url(self.account[0].id)
        res = self.client.get(url)
        self.assertEqual(res.status_code, status.HTTP_200_OK)

        # check if the response returned is in valid format
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

    def test_get_transaction_summary_error_invalid_account(self):
        """Test response for api when account does not exist"""
        url = detail_trx_summary_url('7299be1b-8506-4702-8eb9-c418761f2ddf')
        res = self.client.get(url)
        self.assertEqual(res.status_code, status.HTTP_404_NOT_FOUND)
