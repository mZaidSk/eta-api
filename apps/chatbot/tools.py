from apps.transactions.models import Transaction
from apps.budgets.models import Budget
from django.utils.timezone import now
from django.db.models import Sum


def get_total_expense_this_month(user):
    today = now()
    qs = Transaction.objects.filter(
        user=user, type="expense", date__year=today.year, date__month=today.month
    )
    total = qs.aggregate(Sum("amount"))["amount__sum"] or 0
    return f"Your total expenses for {today.strftime('%B %Y')} are {total}."


def get_total_income_this_month(user):
    today = now()
    qs = Transaction.objects.filter(
        user=user, type="income", date__year=today.year, date__month=today.month
    )
    total = qs.aggregate(Sum("amount"))["amount__sum"] or 0
    return f"Your total income for {today.strftime('%B %Y')} is {total}."
