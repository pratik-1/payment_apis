"""
Serializers for transactions APIs
"""
from core.models import Account, Transaction
from rest_framework import serializers


class AccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account
        fields = "__all__"


class TransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transaction
        fields = "__all__"


class TransactionBalanceSerializer(serializers.Serializer):
    account = AccountSerializer(required=True)
    transactions = serializers.DictField(
        child=serializers.DictField(child=serializers.IntegerField())
    )
    balance = serializers.DictField(child=serializers.IntegerField())
