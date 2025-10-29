from django.urls import path
from .views import (
    summary_view,
    category_breakdown_view,
    budget_vs_actual_view,
    monthly_trend_view,
    financial_health_view,
    spending_trends_view,
    cash_flow_forecast_view,
    budget_burn_rate_view,
    spending_patterns_view,
    category_intelligence_view,
    transaction_statistics_view,
    period_comparison_view,
)

urlpatterns = [
    # Basic Analytics
    path("summary/", summary_view, name="dashboard-summary"),
    path("category-breakdown/", category_breakdown_view, name="dashboard-category-breakdown"),
    path("budget-vs-actual/", budget_vs_actual_view, name="dashboard-budget-vs-actual"),
    path("monthly-trend/", monthly_trend_view, name="dashboard-monthly-trend"),

    # Advanced Analytics
    path("financial-health/", financial_health_view, name="dashboard-financial-health"),
    path("spending-trends/", spending_trends_view, name="dashboard-spending-trends"),
    path("cash-flow-forecast/", cash_flow_forecast_view, name="dashboard-cash-flow-forecast"),
    path("budget-burn-rate/", budget_burn_rate_view, name="dashboard-budget-burn-rate"),
    path("spending-patterns/", spending_patterns_view, name="dashboard-spending-patterns"),
    path("category-intelligence/", category_intelligence_view, name="dashboard-category-intelligence"),
    path("transaction-statistics/", transaction_statistics_view, name="dashboard-transaction-statistics"),
    path("period-comparison/", period_comparison_view, name="dashboard-period-comparison"),
]
