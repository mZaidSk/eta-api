from django.db.models.signals import post_save, post_delete, pre_save
from django.dispatch import receiver
from django.db.models import Sum
from decimal import Decimal
import logging
from .models import Transaction
from apps.budgets.models import Budget
from apps.accounts.models import Account

logger = logging.getLogger(__name__)


# Store old transaction values before update
_transaction_old_values = {}


@receiver(pre_save, sender=Transaction)
def store_old_transaction_values(sender, instance, **kwargs):
    """Store old transaction values before update to properly handle balance changes"""
    if instance.pk:  # Only for updates, not new transactions
        try:
            old_transaction = Transaction.objects.get(pk=instance.pk)
            _transaction_old_values[instance.pk] = {
                'amount': old_transaction.amount,
                'type': old_transaction.type,
                'account_id': old_transaction.account_id,
                'category_id': old_transaction.category_id,
                'date': old_transaction.date
            }
        except Transaction.DoesNotExist:
            pass


@receiver(post_save, sender=Transaction)
def handle_transaction_save(sender, instance, created, **kwargs):
    """Handle account balance and budget updates for transaction create/update"""
    try:
        if created:
            logger.info(f"NEW Transaction created: {instance.type} - {instance.amount} for category {instance.category}")

            # NEW TRANSACTION: Just add the amount to account balance
            account = instance.account
            old_balance = account.balance
            if instance.type == "income":
                account.balance += instance.amount
            elif instance.type == "expense":
                account.balance -= instance.amount
            account.save()
            logger.info(f"Account {account.name} balance updated from {old_balance} to {account.balance}")

            # Update budget for new expense
            if instance.type == "expense" and instance.category:
                logger.info(f"Updating budgets for category {instance.category}")
                update_budgets_for_transaction(instance)

        else:
            # UPDATE TRANSACTION: Revert old, apply new
            if instance.pk in _transaction_old_values:
                old_values = _transaction_old_values[instance.pk]

                # Revert old transaction from old account
                old_account = Account.objects.get(pk=old_values['account_id'])
                if old_values['type'] == "income":
                    old_account.balance -= old_values['amount']
                elif old_values['type'] == "expense":
                    old_account.balance += old_values['amount']
                old_account.save()

                # Apply new transaction to new/same account
                account = instance.account
                if instance.type == "income":
                    account.balance += instance.amount
                elif instance.type == "expense":
                    account.balance -= instance.amount
                account.save()

                # Update budgets if this affects expenses
                if old_values['type'] == 'expense':
                    # Recalculate old category budgets
                    old_budgets = Budget.objects.filter(
                        user=instance.user,
                        category_id=old_values['category_id'],
                        start_date__lte=old_values['date'],
                        end_date__gte=old_values['date']
                    )
                    for budget in old_budgets:
                        recalculate_budget_expense(budget)

                if instance.type == "expense" and instance.category:
                    update_budgets_for_transaction(instance)

                # Clean up stored values
                del _transaction_old_values[instance.pk]

    except Exception as e:
        logger.error(f"Error in handle_transaction_save: {str(e)}", exc_info=True)


@receiver(post_delete, sender=Transaction)
def handle_transaction_delete(sender, instance, **kwargs):
    """Update budget current_expense and account balance when transaction is deleted"""

    # Revert the transaction from account balance
    account = instance.account
    if instance.type == "income":
        account.balance -= instance.amount
    elif instance.type == "expense":
        account.balance += instance.amount
    account.save()

    # Update budget if this was an expense transaction
    if instance.type == "expense" and instance.category:
        budgets = Budget.objects.filter(
            user=instance.user,
            category=instance.category,
            start_date__lte=instance.date,
            end_date__gte=instance.date
        )

        for budget in budgets:
            recalculate_budget_expense(budget)


def update_budgets_for_transaction(transaction):
    """Update all budgets affected by this transaction"""
    try:
        budgets = Budget.objects.filter(
            user=transaction.user,
            category=transaction.category,
            start_date__lte=transaction.date,
            end_date__gte=transaction.date
        )

        logger.info(f"Found {budgets.count()} budgets to update for transaction")

        for budget in budgets:
            recalculate_budget_expense(budget)

    except Exception as e:
        logger.error(f"Error in update_budgets_for_transaction: {str(e)}", exc_info=True)


def recalculate_budget_expense(budget):
    """Recalculate the current_expense for a budget"""
    try:
        old_expense = budget.current_expense

        total_expense = Transaction.objects.filter(
            user=budget.user,
            category=budget.category,
            type="expense",
            date__gte=budget.start_date,
            date__lte=budget.end_date
        ).aggregate(total=Sum("amount"))["total"] or Decimal('0')

        budget.current_expense = total_expense
        budget.save()

        logger.info(
            f"Budget {budget.id} (category: {budget.category}) "
            f"current_expense updated from {old_expense} to {total_expense}"
        )

    except Exception as e:
        logger.error(f"Error in recalculate_budget_expense: {str(e)}", exc_info=True)
