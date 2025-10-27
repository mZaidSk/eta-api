from apps.transactions.models import Transaction
from apps.budgets.models import Budget
from apps.accounts.models import Account
from django.utils.timezone import now
from django.db.models import Sum, Count
from decimal import Decimal


def get_total_expense_this_month(user):
    """Get total expenses for current month"""
    today = now()
    qs = Transaction.objects.filter(
        user=user, type="expense", date__year=today.year, date__month=today.month
    )
    total = qs.aggregate(Sum("amount"))["amount__sum"] or Decimal('0')
    return f"Your total expenses for {today.strftime('%B %Y')} are ${total}."


def get_total_income_this_month(user):
    """Get total income for current month"""
    today = now()
    qs = Transaction.objects.filter(
        user=user, type="income", date__year=today.year, date__month=today.month
    )
    total = qs.aggregate(Sum("amount"))["amount__sum"] or Decimal('0')
    return f"Your total income for {today.strftime('%B %Y')} is ${total}."


def get_category_breakdown(user):
    """Get expense breakdown by category for current month"""
    today = now()
    breakdown = Transaction.objects.filter(
        user=user,
        type="expense",
        date__year=today.year,
        date__month=today.month
    ).values('category__name').annotate(
        total=Sum('amount'),
        count=Count('id')
    ).order_by('-total')

    if not breakdown:
        return "You have no expenses this month yet."

    result = f"Expense breakdown for {today.strftime('%B %Y')}:\n"
    for item in breakdown:
        category = item['category__name'] or 'Uncategorized'
        result += f"- {category}: ${item['total']} ({item['count']} transactions)\n"

    return result


def get_biggest_expense(user):
    """Get the largest expense transaction for current month"""
    today = now()
    transaction = Transaction.objects.filter(
        user=user,
        type="expense",
        date__year=today.year,
        date__month=today.month
    ).order_by('-amount').first()

    if not transaction:
        return "You have no expenses this month."

    return f"Your biggest expense this month is ${transaction.amount} for {transaction.category.name if transaction.category else 'Uncategorized'} on {transaction.date}. Description: {transaction.description or 'No description'}"


def get_budget_status(user):
    """Get status of all active budgets"""
    today = now()
    budgets = Budget.objects.filter(
        user=user,
        start_date__lte=today,
        end_date__gte=today
    ).select_related('category')

    if not budgets:
        return "You have no active budgets set up."

    result = "Your current budget status:\n"
    for budget in budgets:
        remaining = budget.remaining
        percentage_used = (budget.current_expense / budget.amount * 100) if budget.amount > 0 else 0
        status = "⚠️ Over budget!" if remaining < 0 else "✓ On track"

        result += f"- {budget.category.name}: ${budget.current_expense} / ${budget.amount} ({percentage_used:.1f}% used) - {status}\n"

    return result


def get_recent_transactions(user, limit=10):
    """Get recent transactions"""
    transactions = Transaction.objects.filter(
        user=user
    ).select_related('category', 'account').order_by('-date', '-created_at')[:limit]

    if not transactions:
        return "You have no transactions yet."

    result = f"Your last {limit} transactions:\n"
    for t in transactions:
        result += f"- {t.date}: {t.type.title()} ${t.amount} - {t.category.name if t.category else 'Uncategorized'} ({t.account.name})\n"

    return result


def get_account_balances(user):
    """Get balances of all user accounts"""
    accounts = Account.objects.filter(user=user)

    if not accounts:
        return "You have no accounts set up."

    result = "Your account balances:\n"
    total = Decimal('0')
    for account in accounts:
        result += f"- {account.name} ({account.account_type}): ${account.balance}\n"
        total += account.balance

    result += f"\nTotal across all accounts: ${total}"
    return result


def get_spending_trends(user):
    """Get spending comparison between current and last month"""
    today = now()

    # Current month
    current_month_expenses = Transaction.objects.filter(
        user=user,
        type="expense",
        date__year=today.year,
        date__month=today.month
    ).aggregate(total=Sum('amount'))['total'] or Decimal('0')

    # Last month
    if today.month == 1:
        last_month = 12
        last_year = today.year - 1
    else:
        last_month = today.month - 1
        last_year = today.year

    last_month_expenses = Transaction.objects.filter(
        user=user,
        type="expense",
        date__year=last_year,
        date__month=last_month
    ).aggregate(total=Sum('amount'))['total'] or Decimal('0')

    if last_month_expenses == 0:
        return f"Current month expenses: ${current_month_expenses}. No data for last month to compare."

    difference = current_month_expenses - last_month_expenses
    percentage_change = (difference / last_month_expenses * 100) if last_month_expenses > 0 else 0

    trend = "increased" if difference > 0 else "decreased"

    return f"Spending trend: This month ${current_month_expenses} vs last month ${last_month_expenses}. Your spending {trend} by ${abs(difference)} ({abs(percentage_change):.1f}%)."


def get_top_spending_category(user):
    """Get the category with highest spending this month"""
    today = now()
    top_category = Transaction.objects.filter(
        user=user,
        type="expense",
        date__year=today.year,
        date__month=today.month,
        category__isnull=False
    ).values('category__name').annotate(
        total=Sum('amount')
    ).order_by('-total').first()

    if not top_category:
        return "You have no categorized expenses this month."

    return f"Your top spending category this month is {top_category['category__name']} with ${top_category['total']}."
