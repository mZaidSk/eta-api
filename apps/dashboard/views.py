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
