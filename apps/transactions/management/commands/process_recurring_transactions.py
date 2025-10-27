from django.core.management.base import BaseCommand
from django.utils.timezone import now
from django.db import models
from datetime import timedelta
from apps.transactions.models import Transaction, RecurringTransaction


class Command(BaseCommand):
    help = "Process recurring transactions and create actual transactions based on frequency"

    def add_arguments(self, parser):
        parser.add_argument(
            '--dry-run',
            action='store_true',
            help='Show what would be processed without creating transactions',
        )

    def handle(self, *args, **options):
        dry_run = options['dry_run']
        today = now().date()

        self.stdout.write(f"Processing recurring transactions for {today}")

        # Get all active recurring transactions
        recurring_transactions = RecurringTransaction.objects.filter(
            start_date__lte=today
        ).filter(
            models.Q(end_date__isnull=True) | models.Q(end_date__gte=today)
        )

        processed_count = 0
        skipped_count = 0

        for recurring in recurring_transactions:
            # Check if we should process this recurring transaction today
            should_process = self.should_process_today(recurring, today)

            if should_process:
                if dry_run:
                    self.stdout.write(
                        self.style.WARNING(
                            f"[DRY RUN] Would create: {recurring.type} - "
                            f"{recurring.amount} for {recurring.category} "
                            f"via {recurring.account.name}"
                        )
                    )
                else:
                    # Create the actual transaction
                    Transaction.objects.create(
                        user=recurring.user,
                        account=recurring.account,
                        category=recurring.category,
                        type=recurring.type,
                        amount=recurring.amount,
                        description=f"{recurring.description or ''} (Auto-generated from recurring transaction)".strip(),
                        date=today
                    )

                    # Update last_processed_date
                    recurring.last_processed_date = today
                    recurring.save()

                    self.stdout.write(
                        self.style.SUCCESS(
                            f"Created: {recurring.type} - {recurring.amount} for "
                            f"{recurring.category} via {recurring.account.name}"
                        )
                    )

                processed_count += 1
            else:
                skipped_count += 1

        if dry_run:
            self.stdout.write(
                self.style.WARNING(
                    f"\n[DRY RUN] Would process {processed_count} transactions, "
                    f"skipped {skipped_count}"
                )
            )
        else:
            self.stdout.write(
                self.style.SUCCESS(
                    f"\nProcessed {processed_count} recurring transactions, "
                    f"skipped {skipped_count}"
                )
            )

    def should_process_today(self, recurring, today):
        """
        Determine if a recurring transaction should be processed today
        based on its frequency and last_processed_date
        """
        # If never processed and today >= start_date, process it
        if not recurring.last_processed_date:
            return today >= recurring.start_date

        # Calculate the next due date based on frequency
        last_processed = recurring.last_processed_date

        if recurring.frequency == "daily":
            next_due = last_processed + timedelta(days=1)
        elif recurring.frequency == "weekly":
            next_due = last_processed + timedelta(weeks=1)
        elif recurring.frequency == "monthly":
            # Add one month (approximately 30 days, can be refined)
            next_due = last_processed + timedelta(days=30)
        elif recurring.frequency == "yearly":
            next_due = last_processed + timedelta(days=365)
        else:
            return False

        # Process if today is on or after the next due date
        return today >= next_due
