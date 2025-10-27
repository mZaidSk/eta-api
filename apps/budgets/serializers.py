from rest_framework import serializers
from .models import Budget


class BudgetSerializer(serializers.ModelSerializer):
    # Add remaining field as read-only
    remaining = serializers.DecimalField(
        max_digits=12, decimal_places=2, read_only=True
    )

    class Meta:
        model = Budget
        fields = [
            "id",
            "user",
            "category",
            "amount",
            "current_expense",
            "start_date",
            "end_date",
            "created_at",
            "remaining",
        ]
        read_only_fields = ["id", "user", "created_at", "remaining"]
