"""
Models for all apps
"""
from django.db import models
from django.core.validators import MinLengthValidator
import uuid


# Create your models here.
class Account(models.Model):
    """Accounts object."""

    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    name = models.CharField(max_length=255)

    def __str__(self):
        return f"(accountId:{self.id}, Name: {self.name})"


class Transaction(models.Model):
    """Transaction object."""

    id = models.CharField(primary_key=True, max_length=10)
    accountId = models.ForeignKey(Account, on_delete=models.DO_NOTHING)
    amount = models.IntegerField(default=0)
    currency = models.CharField(max_length=3, validators=[MinLengthValidator(3)])
    type = models.CharField(null=False, max_length=20)
    dateTime = models.DateTimeField()

    def __str__(self):
        return f"(accountId: {self.accountId.id}, transaction_id: {self.id})"
