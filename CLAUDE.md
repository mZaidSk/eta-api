# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

ETA API is a Django REST Framework expense tracking application with AI chatbot capabilities. It uses PostgreSQL for data persistence, JWT authentication, and integrates Google Gemini via LangChain for financial insights.

## Development Setup

### Environment Configuration

1. Create a `.env` file with the following variables:
   ```
   DJANGO_SETTINGS_MODULE=eta_api.settings.dev
   POSTGRES_DB=expense_tracker
   POSTGRES_USER=expense_user
   POSTGRES_PASSWORD=password
   POSTGRES_HOST=db
   POSTGRES_PORT=5432
   DJANGO_SECRET_KEY=your-secret-key-here
   GEMINI_API_KEY=your-gemini-api-key
   ```

2. Settings are split across multiple files:
   - `eta_api/settings/base.py` - Common settings
   - `eta_api/settings/dev.py` - Development overrides
   - `eta_api/settings/prod.py` - Production overrides

### Running the Application

**With Docker (Recommended):**
```bash
docker-compose up
```
This starts both the Django app (port 8000) and PostgreSQL (port 3000).

**Without Docker:**
```bash
# Install dependencies
pip install -r requirements.txt

# Run migrations
python manage.py migrate

# Start dev server
python manage.py runserver
```

### Common Commands

```bash
# Create migrations
python manage.py makemigrations

# Apply migrations
python manage.py migrate

# Create superuser
python manage.py createsuperuser

# Django shell
python manage.py shell

# Check for issues
python manage.py check

# Process recurring transactions (creates actual transactions from recurring templates)
python manage.py process_recurring_transactions

# Dry run to see what would be processed
python manage.py process_recurring_transactions --dry-run
```

## Architecture

### App Structure

The project follows Django's app-based architecture with clear separation of concerns:

- **apps/users** - Custom User model with email authentication (uses UUID primary keys)
- **apps/accounts** - Financial accounts (savings, current, credit, cash)
- **apps/categories** - Income/expense categories (user-specific)
- **apps/transactions** - Transactions and RecurringTransactions
- **apps/budgets** - Budget tracking with category-based limits
- **apps/dashboard** - Analytics views (summary, category breakdown, budget vs actual, monthly trends)
- **apps/chatbot** - AI assistant using LangChain + Google Gemini

### Data Model Relationships

```
User (1) ──> (N) Account
User (1) ──> (N) Category
User (1) ──> (N) Budget ──> (1) Category
User (1) ──> (N) Transaction ──> (1) Category
                            └──> (1) Account
User (1) ──> (N) RecurringTransaction ──> (1) Category
                                      └──> (1) Account
```

Key points:
- All models use user-scoped data (foreign key to User)
- Transactions require both a Category and an Account
- Categories can be income or expense type, and include `colorHex` and `icon` fields for UI customization
- Budgets track `current_expense` (auto-updated via signals) and calculate `remaining` as a property
- RecurringTransactions include `type`, `last_processed_date` for automated processing

### URL Routing

Main API routes are namespaced under `/api/`:
- `/api/users/` - Registration, login, profile
- `/api/accounts/` - Account CRUD
- `/api/categories/` - Category CRUD
- `/api/budgets/` - Budget CRUD
- `/api/transactions/` - Transaction CRUD
- `/api/dashboard/` - Analytics endpoints
- `/api/ai/` - Chatbot interaction

All routes are defined in `api/urls.py` which includes individual app URLs.

### Authentication

- Uses `rest_framework_simplejwt` for JWT tokens
- Access token lifetime: 60 minutes
- Refresh token lifetime: 7 days
- Custom User model: `apps.users.User` (email-based authentication)
- Protected views use `@permission_classes([IsAuthenticated])`

### Response Format

Standard response utilities in `eta_api/utils/responses.py`:

**Success Response:**
```json
{
  "success": true,
  "message": "Request successful",
  "data": {...},
  "errors": null,
  "meta": {...}  // optional (pagination, etc.)
}
```

**Error Response:**
```json
{
  "success": false,
  "message": "Error message",
  "data": null,
  "errors": {...},
  "status_code": 400
}
```

Use `success_response()` and `error_response()` helpers from `eta_api.utils.responses`.

### Exception Handling

Custom exception handler in `eta_api/exceptions.py`:
- Wraps DRF's default handler
- Adds `status_code` to all error responses
- Catches non-DRF exceptions and returns 500 responses
- Configured in `REST_FRAMEWORK['EXCEPTION_HANDLER']`

### AI Chatbot Architecture

The chatbot system (`apps/chatbot/`) uses LangChain with Google Gemini:

1. **View Layer** (`views.py`): Handles HTTP requests, fetches user transaction context
2. **Tools** (`tools.py`): Utility functions to query transaction data
3. **Agents** (`agents.py`): LangChain tool wrappers for expense/income queries
4. **LLM** (`llm.py`): Google Gemini model configuration

The chatbot receives the user's last 5 transactions as context and responds to financial queries.

### Dashboard Analytics

Dashboard views (`apps/dashboard/views.py`) support optional `?account=<id>` filtering:
- `summary_view` - Total income, expense, net balance, account balances
- `category_breakdown_view` - Income/expense grouped by category
- `budget_vs_actual_view` - Budget vs actual spending per category
- `monthly_trend_view` - Income/expense trends over time (monthly aggregation)

All use Django ORM aggregations (`Sum`, `TruncMonth`) for efficient queries.

## Automated Data Updates

### Django Signals (apps/transactions/signals.py)

The application uses Django signals to automatically maintain data consistency:

**Budget Expense Updates:**
- When a Transaction is created/updated/deleted, related Budget `current_expense` is automatically recalculated
- Only expense-type transactions within the budget's date range affect the budget
- Signals handle category and date changes properly

**Account Balance Updates:**
- Transaction create: Adds income/subtracts expense from account balance
- Transaction update: Reverts old amount from old account, applies new amount to new account
- Transaction delete: Reverts the transaction amount from account balance
- All operations maintain accurate account balances automatically

**Important:** Do not manually update `Budget.current_expense` or `Account.balance` - they are managed by signals.

### Recurring Transactions

RecurringTransactions are processed via a management command (not automatic):

```bash
# Run daily via cron or task scheduler
python manage.py process_recurring_transactions
```

The command:
- Finds active recurring transactions (start_date <= today, end_date >= today or null)
- Creates actual Transaction records based on frequency (daily, weekly, monthly, yearly)
- Updates `last_processed_date` to prevent duplicates
- Respects the RecurringTransaction `type` field (income or expense)

In production, schedule this command to run daily using:
- **Linux/Mac**: crontab (`0 0 * * * /path/to/python manage.py process_recurring_transactions`)
- **Windows**: Task Scheduler
- **Docker/Kubernetes**: CronJob
- **Celery Beat**: Periodic task

## Important Conventions

1. **Settings Module**: Default is `eta_api.settings.dev` (set in `manage.py`)
2. **User Reference**: Always use `settings.AUTH_USER_MODEL` in foreign keys, not direct User import
3. **UUID Primary Keys**: User model uses UUIDs instead of integer IDs
4. **Database**: PostgreSQL is required (uses psycopg2-binary)
5. **Environment Variables**: All secrets must be in `.env` (never committed)
6. **Custom Table Names**: Models may specify `db_table` in Meta (e.g., User uses "users")
7. **Signals**: Transaction signals automatically update Account balances and Budget expenses - do not modify these fields manually

## Testing

Test files exist but are currently empty stubs. When writing tests:
- Place tests in respective app `tests.py` files
- Use Django's `TestCase` or DRF's `APITestCase`
- Create test users with proper authentication for protected endpoints
