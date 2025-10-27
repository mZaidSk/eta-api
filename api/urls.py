from django.urls import path, include
from .views import health_check

urlpatterns = [
    path("health/", health_check, name="health-check"),
    path("users/", include("apps.users.urls")),
    path("accounts/", include("apps.accounts.urls")),
    path("budgets/", include("apps.budgets.urls")),
    path("categories/", include("apps.categories.urls")),
    path("transactions/", include("apps.transactions.urls")),
    path("dashboard/", include("apps.dashboard.urls")),
    path("ai/", include("apps.chatbot.urls")),
]
