from django.urls import path
from .views import (
    summary_view,
    category_breakdown_view,
    budget_vs_actual_view,
    monthly_trend_view,
)

urlpatterns = [
    path("summary/", summary_view, name="dashboard-summary"),
    path(
        "category-breakdown/",
        category_breakdown_view,
        name="dashboard-category-breakdown",
    ),
    path("budget-vs-actual/", budget_vs_actual_view, name="dashboard-budget-vs-actual"),
    path("monthly-trend/", monthly_trend_view, name="dashboard-monthly-trend"),
]
