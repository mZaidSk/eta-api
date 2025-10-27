from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import TransactionViewSet, RecurringTransactionViewSet

router = DefaultRouter()

router.register(r"trans", TransactionViewSet, basename="transaction")
router.register(
    r"recurring",
    RecurringTransactionViewSet,
    basename="recurring-transaction",
)

urlpatterns = [
    path("", include(router.urls)),
]
