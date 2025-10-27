# Testing Budget & Account Auto-Update Signals

## Prerequisites

1. **Start the database**:
   ```bash
   docker-compose up db -d
   ```

   Or if running locally, make sure PostgreSQL is running.

2. **Apply migrations**:
   ```bash
   python manage.py migrate
   ```

## Quick Test

Run the automated test script:

```bash
python manage.py shell
```

Then in the shell:

```python
from apps.transactions.test_signals import test_budget_update
test_budget_update()
```

This will:
- Create a test user, account, category, and budget
- Create a transaction
- Verify that the budget's `current_expense` is automatically updated
- Verify that the account's `balance` is automatically updated

## Manual Testing via API

### 1. Create required data

**Create a user** (if not exists):
```bash
POST /api/users/register/
{
  "email": "test@example.com",
  "name": "Test User",
  "password": "password123"
}
```

**Login to get token**:
```bash
POST /api/users/login/
{
  "email": "test@example.com",
  "password": "password123"
}
```

**Create an account**:
```bash
POST /api/accounts/
Headers: Authorization: Bearer <your_token>
{
  "name": "My Savings",
  "account_type": "savings",
  "balance": 1000
}
```

**Create a category**:
```bash
POST /api/categories/
Headers: Authorization: Bearer <your_token>
{
  "name": "Groceries",
  "type": "expense",
  "colorHex": "#FF5733",
  "icon": "shopping-cart"
}
```

**Create a budget**:
```bash
POST /api/budgets/
Headers: Authorization: Bearer <your_token>
{
  "category": <category_id>,
  "amount": 500,
  "start_date": "2025-01-01",
  "end_date": "2025-01-31"
}
```

### 2. Check initial values

**Get the budget**:
```bash
GET /api/budgets/<budget_id>/
```

Note the `current_expense` value (should be 0).

**Get the account**:
```bash
GET /api/accounts/<account_id>/
```

Note the `balance` value.

### 3. Create a transaction

```bash
POST /api/transactions/
Headers: Authorization: Bearer <your_token>
{
  "account": <account_id>,
  "category": <category_id>,
  "type": "expense",
  "amount": 50,
  "description": "Test expense",
  "date": "2025-01-15"
}
```

### 4. Verify auto-update

**Check the budget again**:
```bash
GET /api/budgets/<budget_id>/
```

The `current_expense` should now be **50** (or the sum of all expenses in that category within the budget period).

**Check the account again**:
```bash
GET /api/accounts/<account_id>/
```

The `balance` should be reduced by 50 (original balance - 50).

## Viewing Logs

To see detailed logging of signal execution, check the Django console output. You should see messages like:

```
NEW Transaction created: expense - 50 for category Groceries
Account My Savings balance updated from 1000 to 950
Found 1 budgets to update for transaction
Budget 1 (category: Groceries) current_expense updated from 0 to 50
```

## Common Issues

### Issue: Budget not updating

**Possible causes:**
1. **Migrations not applied**: Run `python manage.py migrate`
2. **Transaction date outside budget period**: Make sure the transaction's `date` is between the budget's `start_date` and `end_date`
3. **Wrong category**: Make sure the transaction's category matches the budget's category
4. **Wrong user**: Budgets only update for transactions from the same user
5. **Transaction type is income**: Budgets only track expense transactions

### Issue: Account not updating

**Possible causes:**
1. **Migrations not applied**: Run `python manage.py migrate`
2. **Signals not loaded**: Check that `apps.transactions` is in INSTALLED_APPS

### Issue: Database connection error

If you see "could not translate host name 'db'", it means:
- You're running locally but .env still has `POSTGRES_HOST=db` (Docker hostname)
- Change it to `POSTGRES_HOST=localhost` or `POSTGRES_HOST=127.0.0.1`
- Or start the Docker database: `docker-compose up db -d`

## Debugging

Enable Django logging to see signal execution:

Add to your settings:

```python
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
        },
    },
    'loggers': {
        'apps.transactions.signals': {
            'handlers': ['console'],
            'level': 'INFO',
        },
    },
}
```

Then restart the server and watch the console for signal execution logs.
