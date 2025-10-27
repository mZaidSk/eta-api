"""
Test script to verify that transaction signals are working correctly.

Run this with: python manage.py shell < apps/transactions/test_signals.py

Or in Django shell:
>>> from apps.transactions.test_signals import test_budget_update
>>> test_budget_update()
"""

from django.utils.timezone import now
from django.contrib.auth import get_user_model
from apps.accounts.models import Account
from apps.categories.models import Category
from apps.budgets.models import Budget
from apps.transactions.models import Transaction
from datetime import date, timedelta

User = get_user_model()


def test_budget_update():
    """Test that budget current_expense updates when transaction is created"""

    print("=" * 60)
    print("TESTING BUDGET AUTO-UPDATE SIGNALS")
    print("=" * 60)

    # Get or create a test user
    user, created = User.objects.get_or_create(
        email="test@example.com",
        defaults={"name": "Test User"}
    )
    if created:
        user.set_password("password123")
        user.save()
        print(f"✓ Created test user: {user.email}")
    else:
        print(f"✓ Using existing test user: {user.email}")

    # Create a test account
    account, created = Account.objects.get_or_create(
        user=user,
        name="Test Account",
        defaults={"account_type": "savings", "balance": 1000}
    )
    initial_balance = account.balance
    print(f"✓ Account '{account.name}' initial balance: {initial_balance}")

    # Create a test category
    category, created = Category.objects.get_or_create(
        user=user,
        name="Test Category",
        defaults={"type": "expense", "colorHex": "#FF0000", "icon": "test"}
    )
    print(f"✓ Category '{category.name}' created/found")

    # Create a budget for this category
    today = date.today()
    start_date = today.replace(day=1)
    end_date = (today.replace(day=1) + timedelta(days=32)).replace(day=1) - timedelta(days=1)

    budget, created = Budget.objects.get_or_create(
        user=user,
        category=category,
        start_date=start_date,
        end_date=end_date,
        defaults={"amount": 500}
    )
    initial_expense = budget.current_expense
    print(f"✓ Budget for '{category.name}': {budget.amount}")
    print(f"  Budget period: {budget.start_date} to {budget.end_date}")
    print(f"  Initial current_expense: {initial_expense}")

    # Create a transaction
    transaction_amount = 50
    transaction = Transaction.objects.create(
        user=user,
        account=account,
        category=category,
        type="expense",
        amount=transaction_amount,
        description="Test transaction to verify signals",
        date=today
    )
    print(f"\n✓ Created transaction: {transaction.type} - ${transaction.amount}")

    # Refresh the budget and account from database
    budget.refresh_from_db()
    account.refresh_from_db()

    print("\n" + "=" * 60)
    print("RESULTS:")
    print("=" * 60)

    # Check budget update
    print(f"Budget current_expense:")
    print(f"  Before: {initial_expense}")
    print(f"  After:  {budget.current_expense}")
    print(f"  Expected: {transaction_amount} (or more if there were existing transactions)")

    if budget.current_expense >= transaction_amount:
        print("  ✅ SUCCESS: Budget current_expense updated correctly!")
    else:
        print("  ❌ FAILED: Budget current_expense did NOT update!")

    # Check account balance
    print(f"\nAccount balance:")
    print(f"  Before: {initial_balance}")
    print(f"  After:  {account.balance}")
    print(f"  Expected: {initial_balance - transaction_amount}")

    expected_balance = initial_balance - transaction_amount
    if account.balance == expected_balance:
        print("  ✅ SUCCESS: Account balance updated correctly!")
    else:
        print(f"  ❌ FAILED: Account balance did NOT update correctly!")
        print(f"     Expected: {expected_balance}, Got: {account.balance}")

    print("\n" + "=" * 60)
    print("Budget remaining: ${:.2f}".format(budget.remaining))
    print("=" * 60)

    return budget, account, transaction


if __name__ == "__main__":
    test_budget_update()
