from rest_framework import serializers
from .models import Category


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ["id", "name", "type", "user", "created_at"]
        read_only_fields = ["id", "user", "created_at"]  # 👈 mark as read-only
