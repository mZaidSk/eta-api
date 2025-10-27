from django.db import models
from django.conf import settings


class Category(models.Model):
    CATEGORY_TYPE_CHOICES = [
        ("income", "Income"),
        ("expense", "Expense"),
    ]

    name = models.CharField(max_length=100)
    type = models.CharField(max_length=10, choices=CATEGORY_TYPE_CHOICES)
    colorHex = models.CharField(max_length=7, default="#000000")  # e.g., "#FF5733"
    icon = models.CharField(max_length=50, default="category")  # e.g., "shopping-cart"
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="categories"
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} ({self.type})"
