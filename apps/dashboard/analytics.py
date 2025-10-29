"""
Advanced Analytics Utilities for Dashboard
Provides helper functions for financial calculations and predictions
"""

from decimal import Decimal
from datetime import timedelta, datetime
from django.db.models import Sum, Avg, Count, StdDev, Max, Min
from django.db.models.functions import TruncDay, TruncWeek, TruncMonth
from django.utils.timezone import now
from apps.transactions.models import Transaction
from apps.budgets.models import Budget
from apps.accounts.models import Account
import statistics


def calculate_financial_health_score(user):
    """
    Calculate a financial health score (0-100) based on multiple factors:
    - Savings rate (40 points)
    - Budget adherence (30 points)
    - Spending stability (20 points)
    - Account balance health (10 points)
    """
    score = 0
    details = {}

    # Get current month data
    today = now()
    current_month_transactions = Transaction.objects.filter(
        user=user,
        date__year=today.year,
        date__month=today.month
    )

    # 1. Savings Rate (40 points)
    total_income = current_month_transactions.filter(type='income').aggregate(
        total=Sum('amount'))['total'] or Decimal('0')
    total_expense = current_month_transactions.filter(type='expense').aggregate(
        total=Sum('amount'))['total'] or Decimal('0')

    if total_income > 0:
        savings_rate = ((total_income - total_expense) / total_income) * 100
        # Award points: 0% = 0pts, 20%+ = 40pts
        savings_points = min(40, max(0, (savings_rate / 20) * 40))
        score += savings_points
        details['savings_rate'] = float(savings_rate)
        details['savings_points'] = float(savings_points)
    else:
        details['savings_rate'] = 0
        details['savings_points'] = 0

    # 2. Budget Adherence (30 points)
    active_budgets = Budget.objects.filter(
        user=user,
        start_date__lte=today,
        end_date__gte=today
    )

    if active_budgets.exists():
        budgets_on_track = 0
        total_budgets = active_budgets.count()

        for budget in active_budgets:
            if budget.current_expense <= budget.amount:
                budgets_on_track += 1

        budget_adherence = (budgets_on_track / total_budgets) * 100
        budget_points = (budget_adherence / 100) * 30
        score += budget_points
        details['budget_adherence'] = float(budget_adherence)
        details['budget_points'] = float(budget_points)
    else:
        details['budget_adherence'] = 0
        details['budget_points'] = 0

    # 3. Spending Stability (20 points) - Lower variance is better
    last_3_months_expenses = []
    for i in range(3):
        month_date = today - timedelta(days=30 * i)
        month_expense = Transaction.objects.filter(
            user=user,
            type='expense',
            date__year=month_date.year,
            date__month=month_date.month
        ).aggregate(total=Sum('amount'))['total'] or Decimal('0')
        last_3_months_expenses.append(float(month_expense))

    if len(last_3_months_expenses) > 1 and any(last_3_months_expenses):
        try:
            std_dev = statistics.stdev(last_3_months_expenses)
            mean = statistics.mean(last_3_months_expenses)
            if mean > 0:
                coefficient_of_variation = (std_dev / mean) * 100
                # Lower CV = more stable = more points
                stability_points = max(0, 20 - (coefficient_of_variation / 5))
                score += stability_points
                details['spending_stability'] = float(100 - min(100, coefficient_of_variation))
                details['stability_points'] = float(stability_points)
            else:
                details['spending_stability'] = 100
                details['stability_points'] = 20
        except:
            details['spending_stability'] = 100
            details['stability_points'] = 20
    else:
        details['spending_stability'] = 100
        details['stability_points'] = 20

    # 4. Account Balance Health (10 points)
    total_balance = Account.objects.filter(user=user).aggregate(
        total=Sum('balance'))['total'] or Decimal('0')

    # Positive balance = full points, negative = 0 points
    if total_balance >= 0:
        balance_points = 10
    else:
        balance_points = 0

    score += balance_points
    details['total_balance'] = float(total_balance)
    details['balance_points'] = float(balance_points)

    # Final score
    details['total_score'] = round(score, 2)
    details['rating'] = get_health_rating(score)

    return details


def get_health_rating(score):
    """Convert numeric score to rating"""
    if score >= 80:
        return "Excellent"
    elif score >= 60:
        return "Good"
    elif score >= 40:
        return "Fair"
    elif score >= 20:
        return "Needs Improvement"
    else:
        return "Critical"


def calculate_spending_growth_rate(user, account_id=None):
    """Calculate month-over-month and year-over-year growth rates"""
    today = now()

    # Current month
    current_month = Transaction.objects.filter(
        user=user,
        type='expense',
        date__year=today.year,
        date__month=today.month
    )
    if account_id:
        current_month = current_month.filter(account_id=account_id)
    current_expense = current_month.aggregate(total=Sum('amount'))['total'] or Decimal('0')

    # Last month
    last_month_date = today - timedelta(days=30)
    last_month = Transaction.objects.filter(
        user=user,
        type='expense',
        date__year=last_month_date.year,
        date__month=last_month_date.month
    )
    if account_id:
        last_month = last_month.filter(account_id=account_id)
    last_month_expense = last_month.aggregate(total=Sum('amount'))['total'] or Decimal('0')

    # Month-over-Month growth
    mom_growth = 0
    if last_month_expense > 0:
        mom_growth = ((current_expense - last_month_expense) / last_month_expense) * 100

    # Year-over-Year growth
    last_year_date = today.replace(year=today.year - 1)
    last_year = Transaction.objects.filter(
        user=user,
        type='expense',
        date__year=last_year_date.year,
        date__month=last_year_date.month
    )
    if account_id:
        last_year = last_year.filter(account_id=account_id)
    last_year_expense = last_year.aggregate(total=Sum('amount'))['total'] or Decimal('0')

    yoy_growth = 0
    if last_year_expense > 0:
        yoy_growth = ((current_expense - last_year_expense) / last_year_expense) * 100

    return {
        'current_month': float(current_expense),
        'last_month': float(last_month_expense),
        'mom_growth_rate': round(float(mom_growth), 2),
        'last_year_same_month': float(last_year_expense),
        'yoy_growth_rate': round(float(yoy_growth), 2),
        'trend': 'increasing' if mom_growth > 0 else 'decreasing' if mom_growth < 0 else 'stable'
    }


def forecast_cash_flow(user, months_ahead=3):
    """
    Predict future cash flow based on historical averages
    Simple linear prediction based on last 6 months
    """
    today = now()
    forecasts = []

    # Calculate average monthly income and expense from last 6 months
    monthly_data = []
    for i in range(6):
        month_date = today - timedelta(days=30 * i)
        income = Transaction.objects.filter(
            user=user,
            type='income',
            date__year=month_date.year,
            date__month=month_date.month
        ).aggregate(total=Sum('amount'))['total'] or Decimal('0')

        expense = Transaction.objects.filter(
            user=user,
            type='expense',
            date__year=month_date.year,
            date__month=month_date.month
        ).aggregate(total=Sum('amount'))['total'] or Decimal('0')

        monthly_data.append({
            'income': float(income),
            'expense': float(expense),
            'net': float(income - expense)
        })

    # Calculate averages
    if monthly_data:
        avg_income = statistics.mean([m['income'] for m in monthly_data])
        avg_expense = statistics.mean([m['expense'] for m in monthly_data])
        avg_net = avg_income - avg_expense
    else:
        avg_income = 0
        avg_expense = 0
        avg_net = 0

    # Get current total balance
    current_balance = Account.objects.filter(user=user).aggregate(
        total=Sum('balance'))['total'] or Decimal('0')
    projected_balance = float(current_balance)

    # Generate forecasts
    for i in range(1, months_ahead + 1):
        projected_balance += avg_net
        future_date = today + timedelta(days=30 * i)

        forecasts.append({
            'month': future_date.strftime('%Y-%m'),
            'projected_income': round(avg_income, 2),
            'projected_expense': round(avg_expense, 2),
            'projected_net': round(avg_net, 2),
            'projected_balance': round(projected_balance, 2)
        })

    return {
        'current_balance': float(current_balance),
        'avg_monthly_income': round(avg_income, 2),
        'avg_monthly_expense': round(avg_expense, 2),
        'forecasts': forecasts
    }


def calculate_budget_burn_rate(user):
    """Calculate how fast budgets are being consumed"""
    today = now()
    active_budgets = Budget.objects.filter(
        user=user,
        start_date__lte=today,
        end_date__gte=today
    ).select_related('category')

    burn_rates = []

    for budget in active_budgets:
        # Calculate days elapsed and remaining
        total_days = (budget.end_date - budget.start_date).days + 1
        elapsed_days = (today.date() - budget.start_date).days + 1
        remaining_days = (budget.end_date - today.date()).days

        if elapsed_days > 0:
            # Daily burn rate
            daily_burn = budget.current_expense / elapsed_days

            # Projected total spend if rate continues
            projected_spend = daily_burn * total_days

            # Days until budget exhausted (if over-spending)
            days_to_exhaust = None
            if daily_burn > 0:
                remaining_budget = budget.amount - budget.current_expense
                if remaining_budget > 0:
                    days_to_exhaust = int(remaining_budget / daily_burn)

            # Health status
            percent_used = (budget.current_expense / budget.amount * 100) if budget.amount > 0 else 0
            percent_time_elapsed = (elapsed_days / total_days * 100)

            if percent_used > percent_time_elapsed + 20:
                status = "overspending"
            elif percent_used > percent_time_elapsed:
                status = "on_track_high"
            else:
                status = "on_track"

            burn_rates.append({
                'category': budget.category.name,
                'budget_amount': float(budget.amount),
                'current_expense': float(budget.current_expense),
                'daily_burn_rate': round(float(daily_burn), 2),
                'projected_total': round(float(projected_spend), 2),
                'days_elapsed': elapsed_days,
                'days_remaining': remaining_days,
                'days_to_exhaust': days_to_exhaust,
                'percent_used': round(percent_used, 2),
                'percent_time_elapsed': round(percent_time_elapsed, 2),
                'status': status
            })

    return burn_rates


def analyze_spending_patterns(user, account_id=None):
    """Analyze daily and weekly spending patterns"""
    today = now()
    last_90_days = today - timedelta(days=90)

    transactions = Transaction.objects.filter(
        user=user,
        type='expense',
        date__gte=last_90_days
    )

    if account_id:
        transactions = transactions.filter(account_id=account_id)

    # Daily patterns (day of week)
    daily_data = transactions.annotate(
        day=TruncDay('date')
    ).values('day').annotate(
        total=Sum('amount'),
        count=Count('id')
    ).order_by('day')

    # Group by day of week
    day_of_week_totals = {i: [] for i in range(7)}  # 0=Monday, 6=Sunday

    for item in daily_data:
        day_of_week = item['day'].weekday()
        day_of_week_totals[day_of_week].append(float(item['total']))

    day_names = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
    daily_pattern = []

    for i, day_name in enumerate(day_names):
        if day_of_week_totals[i]:
            avg_spending = statistics.mean(day_of_week_totals[i])
            total_transactions = len(day_of_week_totals[i])
        else:
            avg_spending = 0
            total_transactions = 0

        daily_pattern.append({
            'day': day_name,
            'avg_spending': round(avg_spending, 2),
            'transaction_count': total_transactions
        })

    # Weekly totals
    weekly_data = transactions.annotate(
        week=TruncWeek('date')
    ).values('week').annotate(
        total=Sum('amount'),
        count=Count('id')
    ).order_by('week')

    weekly_pattern = []
    for item in weekly_data:
        weekly_pattern.append({
            'week_start': item['week'].strftime('%Y-%m-%d'),
            'total_spending': float(item['total']),
            'transaction_count': item['count']
        })

    return {
        'daily_pattern': daily_pattern,
        'weekly_pattern': weekly_pattern[-12:]  # Last 12 weeks
    }


def get_category_intelligence(user, account_id=None):
    """Get detailed intelligence about category spending"""
    today = now()
    current_month = Transaction.objects.filter(
        user=user,
        type='expense',
        date__year=today.year,
        date__month=today.month
    )

    if account_id:
        current_month = current_month.filter(account_id=account_id)

    # Category statistics
    category_stats = current_month.values('category__name').annotate(
        total=Sum('amount'),
        count=Count('id'),
        avg=Avg('amount'),
        max=Max('amount'),
        min=Min('amount')
    ).order_by('-total')

    total_spending = sum([float(c['total']) for c in category_stats])

    categories = []
    for cat in category_stats:
        percentage = (float(cat['total']) / total_spending * 100) if total_spending > 0 else 0

        categories.append({
            'category': cat['category__name'] or 'Uncategorized',
            'total_spent': float(cat['total']),
            'percentage_of_total': round(percentage, 2),
            'transaction_count': cat['count'],
            'average_transaction': round(float(cat['avg']), 2),
            'largest_transaction': float(cat['max']),
            'smallest_transaction': float(cat['min'])
        })

    return {
        'total_spending': round(total_spending, 2),
        'category_count': len(categories),
        'categories': categories
    }


def get_transaction_statistics(user, account_id=None, days=30):
    """Get statistical analysis of transactions"""
    today = now()
    start_date = today - timedelta(days=days)

    transactions = Transaction.objects.filter(
        user=user,
        date__gte=start_date
    )

    if account_id:
        transactions = transactions.filter(account_id=account_id)

    # Income statistics
    income_stats = transactions.filter(type='income').aggregate(
        total=Sum('amount'),
        count=Count('id'),
        avg=Avg('amount'),
        max=Max('amount'),
        min=Min('amount')
    )

    # Expense statistics
    expense_stats = transactions.filter(type='expense').aggregate(
        total=Sum('amount'),
        count=Count('id'),
        avg=Avg('amount'),
        max=Max('amount'),
        min=Min('amount'),
        stddev=StdDev('amount')
    )

    # Calculate outliers (transactions > 2 standard deviations from mean)
    outliers = []
    if expense_stats['stddev'] and expense_stats['avg']:
        threshold = float(expense_stats['avg']) + (2 * float(expense_stats['stddev']))
        outlier_transactions = transactions.filter(
            type='expense',
            amount__gte=threshold
        ).values('date', 'amount', 'category__name', 'description')[:10]

        for t in outlier_transactions:
            outliers.append({
                'date': t['date'].strftime('%Y-%m-%d'),
                'amount': float(t['amount']),
                'category': t['category__name'],
                'description': t['description'] or 'No description'
            })

    return {
        'period_days': days,
        'income': {
            'total': float(income_stats['total'] or 0),
            'count': income_stats['count'],
            'average': round(float(income_stats['avg'] or 0), 2),
            'largest': float(income_stats['max'] or 0),
            'smallest': float(income_stats['min'] or 0)
        },
        'expense': {
            'total': float(expense_stats['total'] or 0),
            'count': expense_stats['count'],
            'average': round(float(expense_stats['avg'] or 0), 2),
            'largest': float(expense_stats['max'] or 0),
            'smallest': float(expense_stats['min'] or 0),
            'std_deviation': round(float(expense_stats['stddev'] or 0), 2)
        },
        'outliers': outliers,
        'daily_average_expense': round(float(expense_stats['total'] or 0) / days, 2)
    }
