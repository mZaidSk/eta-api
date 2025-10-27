from rest_framework import serializers
from .models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            "id",
            "name",
            "email",
            "chatbot_enabled",
            "ai_insights_enabled",
            "created_at",
            "last_login",
        ]
