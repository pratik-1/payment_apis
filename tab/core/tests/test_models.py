"""
Tests for models.
"""
from core import models
from django.test import TestCase
from django.core import exceptions
from django.db import utils


class AccountTests(TestCase):
    """Test models."""

    def test_create_account(self):
        """Test creating a account is successful."""

        account = models.Account.objects.create(
            id="7299be1b-8506-4702-8eb9-c418761f2dcf", name="TEST ACCOUNT 1"
        )
        self.assertEqual(account.name, "TEST ACCOUNT 1")

    def test_create_account_failed(self):
        """Test account creation fails due to incorrect input"""
        with self.assertRaises(exceptions.ValidationError):
            models.Account.objects.create(id="7299be1b-8506",
                                          name="TEST ACCOUNT 1")


class TransactionTests(TestCase):
    """Test models."""

    def setUp(self):
        self.account = models.Account.objects.create(
            id="7299be1b-8506-4702-8eb9-c418761f2dcf", name="TEST ACCOUNT 1"
        )

    def test_create_transaction(self):
        """Test creating a account is successful."""
        transaction = models.Transaction.objects.create(
            id="T-01",
            amount=1000000,
            currency="GBP",
            type="Settled",
            dateTime="2021-04-20T15:35:43.964Z",
            accountId=self.account,
        )
        self.assertEqual(transaction.id, "T-01")

    def test_create_transaction_failed_incorrect_type(self):
        """Test Transaction creation fails due to incorrect input type"""
        with self.assertRaises(utils.IntegrityError):
            models.Transaction.objects.create(
                id="T-01",
                amount=1000000,
                currency="G",
                type=None,
                dateTime="2021-04-20T12:08:25+00:00",
                accountId=self.account,
            )

    def test_create_transaction_failed_no_account(self):
        """Test Transaction creation fails due to no account found."""
        with self.assertRaises(utils.IntegrityError):
            models.Transaction.objects.create(
                id="T-01",
                amount=1000000,
                currency="G",
                type="Settled",
                dateTime="2021-04-20T12:08:25+00:00",
                accountId=None,
            )
