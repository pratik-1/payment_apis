"""
Views for Transactions API.
"""
import pandas as pd
from rest_framework import status, viewsets
from rest_framework.views import APIView

from rest_framework.response import Response
from . import serializer
from core.models import Account, Transaction


# Create your views here.
class AccountsView(viewsets.ModelViewSet):
    """Accounts API View"""

    queryset = Account.objects.all()
    serializer_class = serializer.AccountSerializer

    def get_queryset(self):
        return self.queryset.order_by("id")


class TransactionView(viewsets.ModelViewSet):
    """Transaction API View"""

    queryset = Transaction.objects.all()
    serializer_class = serializer.TransactionSerializer

    def get_queryset(self):
        return self.queryset.order_by("id")


def createDictFromPandas(df):
    if df.index.nlevels == 1:
        return df.to_dict()
    dict_f = {}
    for level in df.index.levels[0]:
        if level in df.index:
            dict_f[level] = createDictFromPandas(df.xs((level)))
    return dict_f


class TransactionSummayView(APIView):
    def get_account_object(self, account_id):
        """
        Helper method to get account for a given account_id
        """
        try:
            account = Account.objects.get(id=account_id)
        except Account.DoesNotExist:
            return None
        return account

    def get_transactions_list(self, account_id):
        """Helper method to get transactions for a given account id

        Returns:
            Transactions queryset from database or
        """
        transactions = Transaction.objects.filter(accountId=account_id)
        if not transactions:
            return {}
        return transactions

    def get_transaction_balance(self, account_id):
        """Calculates and return the transaction aggregation for a
        given account id.
        NOTE: This logic may not be desired. May require to change according
        to business requirement.
        Calculation logic:
            `transactions`: grouped by transaction 'type', 'currency'
            and sum over amount to return total within each category.
            For example:
            'transactions': "settled":{
                "GBP":1003000,
                "EUR":200000
                }

            `balance`: grouped by transaction 'currency'
            and sum over amount to return total of each currency.
            For example:
            "balance":{
                "GBP":798700,
                "EUR":139970
                }

        Args:
            account_id (uuid): Account Id
        Returns:
            tuple: transactions, balance
        """
        transactions = self.get_transactions_list(account_id).values()
        balance = {}
        # calculate transactions balance
        if transactions:
            df = pd.DataFrame(list(transactions))
            df["type"] = df["type"].str.lower()

            # transactions aggregation
            agg = df.groupby(["type", "currency"])
            transactions = agg["amount"].sum()
            transactions = createDictFromPandas(transactions)

            # calculate overall balance
            balance = df.groupby(["currency"])["amount"].sum()
            balance = createDictFromPandas(balance)
        return transactions, balance

    def get(self, request, account_id, *args, **kwargs):
        """
        Get View for transaction and balance for the given account id.
        """
        account = self.get_account_object(account_id)
        if not account:
            return Response(
                {"res": f"Account with account id {account_id} does not exists"},
                status=status.HTTP_404_NOT_FOUND,
            )
        transactions, balance = self.get_transaction_balance(account_id)

        d = {"account": account, "transactions": transactions, "balance": balance}
        ser = serializer.TransactionBalanceSerializer(d)
        return Response(ser.data, status=status.HTTP_200_OK)
