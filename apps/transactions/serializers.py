from rest_framework import serializers
from .models import Transaction, RecurringTransaction


class TransactionSerializer(serializers.ModelSerializer):
    category_name = serializers.CharField(source="category.name", read_only=True)
    account_name = serializers.CharField(
        source="account.name", read_only=True
    )  # 👈 add this

    class Meta:
        model = Transaction
        fields = [
            "id",
            "user",
            "account",  # 👈 add account
            "account_name",  # 👈 add account name
            "category",
            "category_name",
            "type",
            "amount",
            "description",
            "date",
            "created_at",
        ]
        read_only_fields = ["id", "user", "created_at", "category_name", "account_name"]


class RecurringTransactionSerializer(serializers.ModelSerializer):
    category_name = serializers.CharField(source="category.name", read_only=True)
    account_name = serializers.CharField(
        source="account.name", read_only=True
    )  # 👈 add this

    class Meta:
        model = RecurringTransaction
        fields = [
            "id",
            "user",
            "account",  # 👈 add account
            "account_name",  # 👈 add account name
            "category",
            "category_name",
            "amount",
            "description",
            "frequency",
            "start_date",
            "end_date",
        ]
        read_only_fields = ["id", "user", "category_name", "account_name"]
