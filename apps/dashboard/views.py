from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from eta_api.utils.responses import success_response
from apps.transactions.models import Transaction
from apps.budgets.models import Budget
from apps.categories.models import Category
from apps.accounts.models import Account
from django.db.models import Sum
from django.db.models.functions import TruncMonth
from django.utils.timezone import now
from .analytics import (
    calculate_financial_health_score,
    calculate_spending_growth_rate,
    forecast_cash_flow,
    calculate_budget_burn_rate,
    analyze_spending_patterns,
    get_category_intelligence,
    get_transaction_statistics
)


# Utility: get filtered transactions by account if account_id provided
def get_transactions(user, account_id=None, type=None):
    qs = Transaction.objects.filter(user=user)
    if account_id:
        qs = qs.filter(account_id=account_id)
    if type:
        qs = qs.filter(type=type)
    return qs


# 1. Dashboard summary
@api_view(["GET"])
@permission_classes([IsAuthenticated])
def summary_view(request):
    user = request.user
    account_id = request.GET.get("account")  # optional filter

    total_income = (
        get_transactions(user, account_id, type="income").aggregate(
            total=Sum("amount")
        )["total"]
        or 0
    )

    total_expense = (
        get_transactions(user, account_id, type="expense").aggregate(
            total=Sum("amount")
        )["total"]
        or 0
    )

    # Optionally show account balances if no filter
    accounts_data = []
    if not account_id:
        for acc in user.accounts.all():
            accounts_data.append(
                {"id": acc.id, "name": acc.name, "balance": acc.balance}
            )

    data = {
        "total_income": total_income,
        "total_expense": total_expense,
        "net_balance": total_income - total_expense,
        "accounts": accounts_data,
    }

    return success_response(data, message="Dashboard summary fetched successfully")


# 2. Category breakdown
@api_view(["GET"])
@permission_classes([IsAuthenticated])
def category_breakdown_view(request):
    user = request.user
    account_id = request.GET.get("account")  # optional filter

    transactions = get_transactions(user, account_id)
    categories = transactions.values("category__name", "type").annotate(
        total=Sum("amount")
    )

    data = {"income": [], "expense": []}
    for c in categories:
        entry = {"category": c["category__name"], "total": c["total"]}
        if c["type"] == "income":
            data["income"].append(entry)
        else:
            data["expense"].append(entry)

    return success_response(data, message="Category breakdown fetched successfully")


# 3. Budget vs Actual
@api_view(["GET"])
@permission_classes([IsAuthenticated])
def budget_vs_actual_view(request):
    user = request.user
    account_id = request.GET.get("account")  # optional filter

    # Budgets by category
    budgets = Budget.objects.filter(user=user).values("category__name", "amount")

    # Actual expenses filtered by account if provided
    actuals = (
        get_transactions(user, account_id, type="expense")
        .values("category__name")
        .annotate(total=Sum("amount"))
    )
    actuals_map = {a["category__name"]: a["total"] for a in actuals}

    data = []
    for b in budgets:
        cat_name = b["category__name"]
        budget_amount = b["amount"]
        actual_spent = actuals_map.get(cat_name, 0)
        data.append(
            {
                "category": cat_name,
                "budget": budget_amount,
                "actual": actual_spent,
                "remaining": budget_amount - actual_spent,
            }
        )

    return success_response(data, message="Budget vs Actual fetched successfully")


# 4. Monthly trend
@api_view(["GET"])
@permission_classes([IsAuthenticated])
def monthly_trend_view(request):
    user = request.user
    account_id = request.GET.get("account")  # optional filter

    transactions = (
        get_transactions(user, account_id)
        .annotate(month=TruncMonth("date"))
        .values("month", "type")
        .annotate(total=Sum("amount"))
        .order_by("month")
    )

    data = {}
    for t in transactions:
        month_str = t["month"].strftime("%Y-%m")
        if month_str not in data:
            data[month_str] = {"month": month_str, "income": 0, "expense": 0}
        data[month_str][t["type"]] = t["total"]

    return success_response(
        list(data.values()), message="Monthly trend fetched successfully"
    )


# 5. Financial Health Score
@api_view(["GET"])
@permission_classes([IsAuthenticated])
def financial_health_view(request):
    """
    Calculate comprehensive financial health score (0-100)
    Based on: savings rate, budget adherence, spending stability, account balance
    """
    user = request.user
    health_data = calculate_financial_health_score(user)
    return success_response(health_data, message="Financial health score calculated successfully")


# 6. Spending Trends & Growth Rates
@api_view(["GET"])
@permission_classes([IsAuthenticated])
def spending_trends_view(request):
    """
    Get month-over-month and year-over-year spending growth rates
    Supports optional account filtering
    """
    user = request.user
    account_id = request.GET.get("account")
    trends_data = calculate_spending_growth_rate(user, account_id)
    return success_response(trends_data, message="Spending trends fetched successfully")


# 7. Cash Flow Forecast
@api_view(["GET"])
@permission_classes([IsAuthenticated])
def cash_flow_forecast_view(request):
    """
    Predict future cash flow for next 3-6 months based on historical averages
    Query param: months (default: 3, max: 12)
    """
    user = request.user
    months_ahead = int(request.GET.get("months", 3))
    months_ahead = min(months_ahead, 12)  # Cap at 12 months

    forecast_data = forecast_cash_flow(user, months_ahead)
    return success_response(forecast_data, message="Cash flow forecast generated successfully")


# 8. Budget Performance & Burn Rate
@api_view(["GET"])
@permission_classes([IsAuthenticated])
def budget_burn_rate_view(request):
    """
    Analyze budget consumption rate and predict exhaustion date
    Shows daily burn rate and spending velocity
    """
    user = request.user
    burn_rate_data = calculate_budget_burn_rate(user)
    return success_response(burn_rate_data, message="Budget burn rate calculated successfully")


# 9. Spending Patterns (Daily/Weekly)
@api_view(["GET"])
@permission_classes([IsAuthenticated])
def spending_patterns_view(request):
    """
    Analyze spending patterns by day of week and weekly trends
    Shows when user spends the most (last 90 days)
    """
    user = request.user
    account_id = request.GET.get("account")
    patterns_data = analyze_spending_patterns(user, account_id)
    return success_response(patterns_data, message="Spending patterns analyzed successfully")


# 10. Category Intelligence
@api_view(["GET"])
@permission_classes([IsAuthenticated])
def category_intelligence_view(request):
    """
    Detailed category-wise spending analysis
    Includes percentages, averages, and transaction statistics per category
    """
    user = request.user
    account_id = request.GET.get("account")
    intelligence_data = get_category_intelligence(user, account_id)
    return success_response(intelligence_data, message="Category intelligence fetched successfully")


# 11. Transaction Statistics & Outliers
@api_view(["GET"])
@permission_classes([IsAuthenticated])
def transaction_statistics_view(request):
    """
    Statistical analysis of transactions with outlier detection
    Query param: days (default: 30, max: 365)
    """
    user = request.user
    account_id = request.GET.get("account")
    days = int(request.GET.get("days", 30))
    days = min(days, 365)  # Cap at 1 year

    stats_data = get_transaction_statistics(user, account_id, days)
    return success_response(stats_data, message="Transaction statistics calculated successfully")


# 12. Period Comparison (Custom Date Ranges)
@api_view(["GET"])
@permission_classes([IsAuthenticated])
def period_comparison_view(request):
    """
    Compare spending/income between two custom date periods
    Query params:
    - period1_start, period1_end (required)
    - period2_start, period2_end (required)
    - account (optional)
    """
    from datetime import datetime

    user = request.user
    account_id = request.GET.get("account")

    try:
        # Parse period 1
        period1_start = datetime.strptime(request.GET.get("period1_start"), "%Y-%m-%d").date()
        period1_end = datetime.strptime(request.GET.get("period1_end"), "%Y-%m-%d").date()

        # Parse period 2
        period2_start = datetime.strptime(request.GET.get("period2_start"), "%Y-%m-%d").date()
        period2_end = datetime.strptime(request.GET.get("period2_end"), "%Y-%m-%d").date()

        # Get transactions for period 1
        period1_transactions = Transaction.objects.filter(
            user=user,
            date__gte=period1_start,
            date__lte=period1_end
        )
        if account_id:
            period1_transactions = period1_transactions.filter(account_id=account_id)

        period1_income = period1_transactions.filter(type='income').aggregate(
            total=Sum('amount'))['total'] or 0
        period1_expense = period1_transactions.filter(type='expense').aggregate(
            total=Sum('amount'))['total'] or 0

        # Get transactions for period 2
        period2_transactions = Transaction.objects.filter(
            user=user,
            date__gte=period2_start,
            date__lte=period2_end
        )
        if account_id:
            period2_transactions = period2_transactions.filter(account_id=account_id)

        period2_income = period2_transactions.filter(type='income').aggregate(
            total=Sum('amount'))['total'] or 0
        period2_expense = period2_transactions.filter(type='expense').aggregate(
            total=Sum('amount'))['total'] or 0

        # Calculate differences
        income_diff = period2_income - period1_income
        expense_diff = period2_expense - period1_expense

        income_change_pct = (income_diff / period1_income * 100) if period1_income > 0 else 0
        expense_change_pct = (expense_diff / period1_expense * 100) if period1_expense > 0 else 0

        data = {
            "period1": {
                "start_date": period1_start.strftime("%Y-%m-%d"),
                "end_date": period1_end.strftime("%Y-%m-%d"),
                "income": float(period1_income),
                "expense": float(period1_expense),
                "net": float(period1_income - period1_expense)
            },
            "period2": {
                "start_date": period2_start.strftime("%Y-%m-%d"),
                "end_date": period2_end.strftime("%Y-%m-%d"),
                "income": float(period2_income),
                "expense": float(period2_expense),
                "net": float(period2_income - period2_expense)
            },
            "comparison": {
                "income_difference": float(income_diff),
                "income_change_percent": round(float(income_change_pct), 2),
                "expense_difference": float(expense_diff),
                "expense_change_percent": round(float(expense_change_pct), 2)
            }
        }

        return success_response(data, message="Period comparison completed successfully")

    except (ValueError, TypeError) as e:
        return success_response(
            None,
            message=f"Invalid date format. Use YYYY-MM-DD format. Error: {str(e)}",
            status=400
        )
