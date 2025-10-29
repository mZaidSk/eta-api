# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

**ETA API** is a production-ready Django REST Framework-based expense tracking application with AI-powered financial insights. The application provides comprehensive financial management capabilities including multi-account tracking, automated budget monitoring, recurring transaction processing, advanced analytics (12+ endpoints), and an intelligent chatbot assistant powered by Google Gemini 2.0 Flash via LangChain.

### Technology Stack

**Core Framework:**
- Django 5.2.5 - High-level Python web framework
- Django REST Framework 3.16.1 - RESTful API toolkit
- PostgreSQL 15 - Primary relational database
- psycopg2-binary 2.9.10 - PostgreSQL adapter

**Authentication & Security:**
- djangorestframework-simplejwt 5.5.1 - JWT token authentication
- Access token lifetime: 60 minutes
- Refresh token lifetime: 7 days
- Email-based authentication (not username)
- User model uses UUID primary keys

**AI/LLM Integration:**
- LangChain 0.3.27 - LLM application framework
- LangChain Google GenAI 2.1.10 - Google AI integration
- Google Gemini 2.0 Flash Experimental - Conversational AI model
- google-genai 1.33.0 - Google AI Python SDK
- Temperature: 0.7, Max iterations: 5

**Data & Analytics:**
- numpy 2.3.2 - Numerical computing for analytics
- Pydantic 2.11.7 - Data validation
- SQLAlchemy 2.0.43 - SQL toolkit (for advanced queries)

**Development Tools:**
- Docker & Docker Compose - Containerization
- python-dotenv 1.1.1 - Environment management
- Gunicorn - Production WSGI server

### Key Features

1. **Multi-Account Financial Tracking** - Track income and expenses across savings, checking, credit, and cash accounts with automatic balance updates
2. **Smart Budget Management** - Category-based budgets with real-time tracking, burn rate analysis, and automatic expense calculation via Django signals
3. **AI Financial Assistant** - Natural language chatbot with 9 specialized tools for financial queries, powered by Google Gemini
4. **Advanced Analytics Dashboard** - 12+ endpoints including financial health scoring (0-100), cash flow forecasting (1-12 months), spending patterns, outlier detection, and period comparisons
5. **Automated Transaction Processing** - Recurring transactions (daily/weekly/monthly/yearly) with management command automation
6. **Data Consistency via Signals** - Automatic updates to account balances and budget expenses without manual intervention
7. **User Data Privacy** - All data scoped per user with JWT authentication and user-specific querysets

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

The chatbot system (`apps/chatbot/`) uses LangChain with Google Gemini 2.0 Flash:

**Architecture Layers:**
1. **View Layer** (`views.py`): Handles HTTP requests, manages conversations, fetches user context
2. **Tools** (`tools.py`): 9 specialized financial data query functions
3. **Agents** (`agents.py`): LangChain tool wrappers and agent initialization
4. **LLM Configuration** (`llm.py`): Google Gemini model setup (temperature: 0.7)

**Models** (`models.py`):
- `Conversation`: Stores conversation threads with auto-generated titles
- `ChatMessage`: Stores individual messages with roles (user/assistant/system)

**Available Tools (9 total):**
1. `expense_tool` - Total expenses for current month
2. `income_tool` - Total income for current month
3. `category_breakdown_tool` - Expense breakdown by category
4. `biggest_expense_tool` - Largest single expense transaction
5. `budget_status_tool` - Active budget status and over-budget alerts
6. `recent_transactions_tool` - Last 10 transactions
7. `account_balances_tool` - All account balances and total
8. `spending_trends_tool` - Month-over-month spending comparison
9. `top_spending_category_tool` - Highest spending category

**API Endpoints:**
- `POST /api/ai/chat/` - Send message to chatbot (with optional conversation_id)
- `GET /api/ai/conversations/` - List user's conversations
- `POST /api/ai/conversations/create/` - Create new conversation
- `GET /api/ai/conversations/{id}/` - Get conversation with messages
- `DELETE /api/ai/conversations/{id}/delete/` - Delete conversation

**How It Works:**
1. User sends message via `/api/ai/chat/`
2. System loads conversation context (last 10 messages)
3. LangChain agent analyzes query and determines required tools
4. Agent calls tools to fetch data from Django ORM
5. AI generates natural language response based on tool results
6. Response saved to ChatMessage and returned to user

**Configuration:**
- Model: Gemini 2.0 Flash Experimental
- Temperature: 0.7 (balanced creativity and accuracy)
- Max iterations: 5 tool calls per query
- Context window: Last 10 messages
- Auto-titled conversations from first message

The chatbot provides intelligent financial insights through natural language queries without requiring users to navigate complex dashboards.

### Dashboard Analytics

Dashboard provides 12+ analytical endpoints (`apps/dashboard/views.py`):

**Basic Analytics (4 endpoints):**
- `summary_view` - Total income, expense, net balance, account balances
- `category_breakdown_view` - Income/expense grouped by category
- `budget_vs_actual_view` - Budget vs actual spending per category with remaining amounts
- `monthly_trend_view` - Income/expense trends over time (monthly aggregation)

**Advanced Analytics (8 endpoints):**
- `financial_health_view` - 0-100 score based on savings rate (40%), budget adherence (30%), spending stability (20%), and account balance health (10%)
- `spending_trends_view` - Month-over-month and year-over-year growth rates
- `cash_flow_forecast_view` - Projects income/expense for 1-12 months based on historical averages (parameter: `?months=6`)
- `budget_burn_rate_view` - Daily consumption rate, days until budget exhaustion, over-budget alerts
- `spending_patterns_view` - Daily (by day of week) and weekly spending pattern analysis
- `category_intelligence_view` - Detailed category statistics with percentages, averages, transaction counts
- `transaction_statistics_view` - Statistical analysis (mean, median, std dev) with outlier detection (>2 std deviations) (parameter: `?days=30`)
- `period_comparison_view` - Compare two custom date ranges side-by-side (parameters: `period1_start`, `period1_end`, `period2_start`, `period2_end`)

**Query Parameters:**
- `?account=<id>` - Filter by specific account (optional, applies to most endpoints)
- `?months=<1-12>` - Number of forecast months (cash flow forecast)
- `?days=<1-365>` - Analysis period for statistics

**Analytics Functions** (`apps/dashboard/analytics.py`):
- `calculate_financial_health_score(user)` - Returns score (0-100) and rating
- `calculate_spending_growth_rate(user, account_id)` - MoM/YoY rates
- `forecast_cash_flow(user, months_ahead)` - Future projections
- `calculate_budget_burn_rate(user)` - Consumption analysis
- `analyze_spending_patterns(user, account_id)` - Pattern detection
- `get_category_intelligence(user, account_id)` - Category insights
- `get_transaction_statistics(user, account_id, days)` - Statistical analysis

All use Django ORM aggregations (`Sum`, `Avg`, `Count`, `TruncMonth`, `TruncDate`) for efficient queries.

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

## Complete API Endpoint Reference

Base URL: `/api/`

### Health Check
- `GET /api/health/` - API health check endpoint

### User Management (apps/users)
- `POST /api/users/register/` - Register new user
- `POST /api/users/login/` - Login and receive JWT tokens
- `GET /api/users/profile/` - Get current user profile
- `PUT /api/users/profile/` - Update user profile

### Accounts (apps/accounts)
- `GET /api/accounts/` - List user's accounts
- `POST /api/accounts/` - Create new account
- `GET /api/accounts/{id}/` - Retrieve account details
- `PUT /api/accounts/{id}/` - Update account
- `PATCH /api/accounts/{id}/` - Partial update account
- `DELETE /api/accounts/{id}/` - Delete account

### Categories (apps/categories)
- `GET /api/categories/` - List user's categories
- `POST /api/categories/` - Create new category
- `GET /api/categories/{id}/` - Retrieve category details
- `PUT /api/categories/{id}/` - Update category
- `PATCH /api/categories/{id}/` - Partial update category
- `DELETE /api/categories/{id}/` - Delete category

### Transactions (apps/transactions)
- `GET /api/transactions/trans/` - List transactions
- `POST /api/transactions/trans/` - Create new transaction
- `GET /api/transactions/trans/{id}/` - Retrieve transaction
- `PUT /api/transactions/trans/{id}/` - Update transaction
- `PATCH /api/transactions/trans/{id}/` - Partial update transaction
- `DELETE /api/transactions/trans/{id}/` - Delete transaction

### Recurring Transactions (apps/transactions)
- `GET /api/transactions/recurring/` - List recurring transactions
- `POST /api/transactions/recurring/` - Create recurring transaction
- `GET /api/transactions/recurring/{id}/` - Retrieve recurring transaction
- `PUT /api/transactions/recurring/{id}/` - Update recurring transaction
- `PATCH /api/transactions/recurring/{id}/` - Partial update recurring transaction
- `DELETE /api/transactions/recurring/{id}/` - Delete recurring transaction

### Budgets (apps/budgets)
- `GET /api/budgets/` - List user's budgets
- `POST /api/budgets/` - Create new budget
- `GET /api/budgets/{id}/` - Retrieve budget details
- `PUT /api/budgets/{id}/` - Update budget
- `PATCH /api/budgets/{id}/` - Partial update budget
- `DELETE /api/budgets/{id}/` - Delete budget

### Dashboard Analytics (apps/dashboard) - 12 Endpoints
- `GET /api/dashboard/summary/` - Overall financial summary
- `GET /api/dashboard/category-breakdown/` - Spending by category
- `GET /api/dashboard/budget-vs-actual/` - Budget comparison
- `GET /api/dashboard/monthly-trend/` - Monthly trends
- `GET /api/dashboard/financial-health/` - Health score (0-100)
- `GET /api/dashboard/spending-trends/` - MoM/YoY growth
- `GET /api/dashboard/cash-flow-forecast/` - Future projections
- `GET /api/dashboard/budget-burn-rate/` - Burn rate analysis
- `GET /api/dashboard/spending-patterns/` - Pattern analysis
- `GET /api/dashboard/category-intelligence/` - Category insights
- `GET /api/dashboard/transaction-statistics/` - Statistical analysis
- `GET /api/dashboard/period-comparison/` - Period comparison

### AI Chatbot (apps/chatbot)
- `POST /api/ai/chat/` - Send message to chatbot
- `GET /api/ai/conversations/` - List conversations
- `POST /api/ai/conversations/create/` - Create new conversation
- `GET /api/ai/conversations/{id}/` - Get conversation with messages
- `DELETE /api/ai/conversations/{id}/delete/` - Delete conversation

**Total: 51+ API endpoints** with full CRUD operations for core models.

## File Structure Reference

```
eta-api/
├── manage.py                          # Django management script
├── requirements.txt                   # Python dependencies
├── docker-compose.yml                 # Docker orchestration
├── docker-compose.override.yml        # Docker dev overrides
├── Dockerfile                         # Production Docker image
├── Dockerfile.dev                     # Development Docker image
├── .env                               # Environment variables (not committed)
├── .gitignore                         # Git ignore patterns
│
├── eta_api/                           # Django project configuration
│   ├── __init__.py
│   ├── asgi.py                        # ASGI configuration
│   ├── wsgi.py                        # WSGI configuration
│   ├── urls.py                        # Main URL router
│   ├── exceptions.py                  # Custom exception handler
│   ├── settings/                      # Environment-specific settings
│   │   ├── __init__.py
│   │   ├── base.py                    # Common settings
│   │   ├── dev.py                     # Development overrides
│   │   └── prod.py                    # Production overrides
│   └── utils/                         # Utility modules
│       ├── __init__.py
│       ├── responses.py               # Standard response helpers
│       └── exceptions.py              # Exception utilities
│
├── api/                               # API router application
│   ├── __init__.py
│   ├── urls.py                        # Main API URL configuration
│   └── views.py                       # Health check endpoint
│
├── apps/                              # Django applications
│   ├── __init__.py
│   │
│   ├── users/                         # User management
│   │   ├── __init__.py
│   │   ├── models.py                  # Custom User model (UUID, email auth)
│   │   ├── views.py                   # Registration, login, profile
│   │   ├── serializers.py             # User serializers
│   │   ├── urls.py                    # User routes
│   │   ├── admin.py                   # Admin configuration
│   │   ├── apps.py                    # App configuration
│   │   ├── migrations/                # Database migrations
│   │   └── tests.py                   # Unit tests
│   │
│   ├── accounts/                      # Financial accounts
│   │   ├── models.py                  # Account model
│   │   ├── views.py                   # AccountViewSet
│   │   ├── serializers.py             # Account serializers
│   │   ├── urls.py                    # Account routes
│   │   ├── admin.py
│   │   ├── apps.py
│   │   ├── migrations/
│   │   └── tests.py
│   │
│   ├── categories/                    # Categories
│   │   ├── models.py                  # Category model (with colorHex, icon)
│   │   ├── views.py                   # CategoryViewSet
│   │   ├── serializers.py             # Category serializers
│   │   ├── urls.py                    # Category routes
│   │   ├── admin.py
│   │   ├── apps.py
│   │   ├── migrations/
│   │   └── tests.py
│   │
│   ├── transactions/                  # Transactions
│   │   ├── models.py                  # Transaction, RecurringTransaction
│   │   ├── views.py                   # Transaction ViewSets
│   │   ├── serializers.py             # Transaction serializers
│   │   ├── urls.py                    # Transaction routes
│   │   ├── signals.py                 # Auto-update signals
│   │   ├── admin.py
│   │   ├── apps.py                    # Signal registration
│   │   ├── migrations/
│   │   ├── tests.py
│   │   └── management/
│   │       └── commands/
│   │           └── process_recurring_transactions.py
│   │
│   ├── budgets/                       # Budgets
│   │   ├── models.py                  # Budget model
│   │   ├── views.py                   # BudgetViewSet
│   │   ├── serializers.py             # Budget serializers
│   │   ├── urls.py                    # Budget routes
│   │   ├── admin.py
│   │   ├── apps.py
│   │   ├── migrations/
│   │   └── tests.py
│   │
│   ├── dashboard/                     # Analytics
│   │   ├── views.py                   # 12 analytical endpoints
│   │   ├── analytics.py               # Calculation functions
│   │   ├── urls.py                    # Dashboard routes
│   │   ├── admin.py
│   │   ├── apps.py
│   │   ├── migrations/
│   │   └── tests.py
│   │
│   └── chatbot/                       # AI Assistant
│       ├── models.py                  # Conversation, ChatMessage
│       ├── views.py                   # Chatbot endpoints
│       ├── agents.py                  # LangChain agent setup
│       ├── tools.py                   # 9 financial tools
│       ├── llm.py                     # Gemini configuration
│       ├── serializers.py             # Chatbot serializers
│       ├── urls.py                    # Chatbot routes
│       ├── admin.py
│       ├── apps.py
│       ├── ollama_client.py           # Alternative LLM option
│       ├── migrations/
│       └── tests.py
│
├── CLAUDE.md                          # Developer guide (this file)
├── README.md                          # Project documentation
├── CHATBOT_API_GUIDE.md               # Chatbot API documentation
├── DASHBOARD_API_GUIDE.md             # Dashboard API documentation
├── TESTING_SIGNALS.md                 # Signal testing guide
└── venv/                              # Virtual environment (not committed)
```

## Important Conventions

1. **Settings Module**: Default is `eta_api.settings.dev` (set in `manage.py`)
2. **User Reference**: Always use `settings.AUTH_USER_MODEL` in foreign keys, not direct User import
3. **UUID Primary Keys**: User model uses UUIDs instead of integer IDs
4. **Database**: PostgreSQL is required (uses psycopg2-binary)
5. **Environment Variables**: All secrets must be in `.env` (never committed)
6. **Custom Table Names**: Models may specify `db_table` in Meta (e.g., User uses "users")
7. **Signals**: Transaction signals automatically update Account balances and Budget expenses - do not modify these fields manually
8. **Response Format**: Always use `success_response()` and `error_response()` helpers from `eta_api.utils.responses`
9. **User Scoping**: Filter all querysets with `filter(user=self.request.user)` to ensure data privacy
10. **Permission Classes**: Use `permission_classes = [permissions.IsAuthenticated]` for protected endpoints

## Model Field Details

### User Model (apps/users/models.py)
- `id` (UUID, primary key) - Unique identifier
- `email` (EmailField, unique) - Authentication credential
- `name` (CharField) - User's display name
- `password` (CharField) - Hashed password
- `is_active` (BooleanField) - Account status
- `is_staff` (BooleanField) - Admin access
- `created_at` (DateTimeField) - Registration timestamp
- `last_login` (DateTimeField) - Last login timestamp
- `chatbot_enabled` (BooleanField) - Chatbot feature flag
- `ai_insights_enabled` (BooleanField) - AI insights feature flag

### Account Model (apps/accounts/models.py)
- `id` (UUID, primary key)
- `user` (ForeignKey to User)
- `name` (CharField) - Account name
- `account_type` (CharField) - Choices: savings, current, credit, cash, other
- `balance` (DecimalField, max_digits=12, decimal_places=2) - Auto-updated via signals
- `created_at` (DateTimeField)

### Category Model (apps/categories/models.py)
- `id` (UUID, primary key)
- `user` (ForeignKey to User)
- `name` (CharField) - Category name
- `type` (CharField) - Choices: income, expense
- `colorHex` (CharField) - Hex color code (e.g., "#FF5733") for UI
- `icon` (CharField) - Icon identifier (e.g., "shopping-cart") for UI
- `created_at` (DateTimeField)

### Transaction Model (apps/transactions/models.py)
- `id` (UUID, primary key)
- `user` (ForeignKey to User)
- `account` (ForeignKey to Account)
- `category` (ForeignKey to Category, nullable)
- `type` (CharField) - Choices: income, expense
- `amount` (DecimalField, max_digits=12, decimal_places=2)
- `description` (TextField, optional)
- `date` (DateField) - Transaction date
- `created_at` (DateTimeField)

### RecurringTransaction Model (apps/transactions/models.py)
- `id` (UUID, primary key)
- `user` (ForeignKey to User)
- `account` (ForeignKey to Account)
- `category` (ForeignKey to Category, nullable)
- `type` (CharField) - Choices: income, expense
- `amount` (DecimalField, max_digits=12, decimal_places=2)
- `description` (TextField, optional)
- `frequency` (CharField) - Choices: daily, weekly, monthly, yearly
- `start_date` (DateField) - When recurring starts
- `end_date` (DateField, nullable) - When recurring ends (null = indefinite)
- `last_processed_date` (DateField, nullable) - Last creation date
- `created_at` (DateTimeField)

### Budget Model (apps/budgets/models.py)
- `id` (UUID, primary key)
- `user` (ForeignKey to User)
- `category` (ForeignKey to Category)
- `amount` (DecimalField, max_digits=12, decimal_places=2) - Budget limit
- `current_expense` (DecimalField, max_digits=12, decimal_places=2) - Auto-calculated via signals
- `start_date` (DateField) - Budget period start
- `end_date` (DateField) - Budget period end
- `created_at` (DateTimeField)
- **Property**: `remaining` - Returns (amount - current_expense)

### Conversation Model (apps/chatbot/models.py)
- `id` (UUID, primary key)
- `user` (ForeignKey to User)
- `title` (CharField) - Auto-generated from first message
- `created_at` (DateTimeField)
- `updated_at` (DateTimeField)

### ChatMessage Model (apps/chatbot/models.py)
- `id` (UUID, primary key)
- `conversation` (ForeignKey to Conversation)
- `role` (CharField) - Choices: user, assistant, system
- `content` (TextField) - Message text
- `created_at` (DateTimeField)

## Testing

Test files exist but are currently empty stubs. When writing tests:
- Place tests in respective app `tests.py` files
- Use Django's `TestCase` or DRF's `APITestCase`
- Create test users with proper authentication for protected endpoints
- Use `self.client.force_authenticate(user=self.user)` for authenticated requests
- Test signal behavior by verifying auto-updated fields (balance, current_expense)
- Test user scoping to ensure users cannot access others' data

**Example Test Structure:**
```python
from rest_framework.test import APITestCase
from rest_framework import status
from apps.users.models import User

class TransactionTestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            email='test@example.com',
            password='testpass123'
        )
        self.client.force_authenticate(user=self.user)

    def test_create_transaction(self):
        response = self.client.post('/api/transactions/trans/', {
            'account': str(account_uuid),
            'category': str(category_uuid),
            'type': 'expense',
            'amount': 100.00,
            'date': '2025-10-30'
        })
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
```

## Additional Documentation

For more detailed information, refer to:
- **README.md** - Comprehensive project documentation for users and developers
- **CHATBOT_API_GUIDE.md** - Detailed chatbot API documentation with examples
- **DASHBOARD_API_GUIDE.md** - Dashboard analytics endpoint documentation
- **TESTING_SIGNALS.md** - Signal testing guide and troubleshooting
