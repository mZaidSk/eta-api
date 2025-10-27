from django.db import models
from django.conf import settings
from apps.categories.models import Category


class Budget(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="budgets"
    )
    category = models.ForeignKey(
        Category, on_delete=models.CASCADE, related_name="budgets"
    )
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    current_expense = models.DecimalField(
        max_digits=12, decimal_places=2, default=0
    )  # new field
    start_date = models.DateField()
    end_date = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Budget {self.category.name} - {self.amount}"

    @property
    def remaining(self):
        return self.amount - self.current_expense
