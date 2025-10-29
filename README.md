# ETA API - Expense Tracking Application

A comprehensive Django REST Framework-based expense tracking application with AI-powered financial insights, real-time budget tracking, and advanced analytics.

## Table of Contents

- [Overview](#overview)
- [Key Features](#key-features)
- [Technology Stack](#technology-stack)
- [Project Architecture](#project-architecture)
- [Getting Started](#getting-started)
- [API Documentation](#api-documentation)
- [Database Schema](#database-schema)
- [AI Chatbot](#ai-chatbot)
- [Dashboard Analytics](#dashboard-analytics)
- [Automated Systems](#automated-systems)
- [Development](#development)
- [Deployment](#deployment)
- [Contributing](#contributing)
- [License](#license)

## Overview

**ETA API** is a full-featured financial management system built with Django and Django REST Framework. It helps users track expenses, manage budgets, analyze spending patterns, and receive AI-powered financial insights through an intelligent chatbot powered by Google Gemini.

### Why ETA API?

- **Real-time Financial Tracking**: Monitor income and expenses across multiple accounts
- **Smart Budget Management**: Set category-based budgets with automatic tracking
- **AI-Powered Insights**: Natural language financial queries with Google Gemini 2.0 Flash
- **Advanced Analytics**: 12+ analytical endpoints including health score, forecasting, and trend analysis
- **Automated Data Updates**: Django signals automatically maintain data consistency
- **Recurring Transactions**: Automate regular income and expense entries
- **User-Scoped Privacy**: All data isolated per user with JWT authentication

## Key Features

### 1. Financial Account Management
- Support for multiple account types (savings, checking, credit, cash)
- Automatic balance updates via Django signals
- Real-time account summaries and balance tracking

### 2. Transaction Tracking
- One-time and recurring transaction support
- Income and expense categorization
- Transaction history with filtering capabilities
- Automatic processing of recurring transactions

### 3. Budget Management
- Per-category budget limits with date ranges
- Real-time budget tracking and remaining balance calculation
- Budget burn rate analysis and exhaustion predictions
- Over-budget alerts and insights

### 4. AI Chatbot Assistant
- **9 Specialized Financial Tools**:
  - Total expense and income queries
  - Category breakdown analysis
  - Biggest expense identification
  - Budget status monitoring
  - Recent transaction retrieval
  - Account balance summaries
  - Spending trend analysis
  - Top spending category identification
- Natural language conversation interface
- Multi-turn conversation context with history
- Powered by Google Gemini 2.0 Flash via LangChain

### 5. Comprehensive Analytics Dashboard
**12+ Analytical Endpoints**:
- **Summary View**: Total income, expense, net balance, account balances
- **Category Breakdown**: Income/expense grouped by category
- **Budget vs Actual**: Budget comparison with remaining amounts
- **Monthly Trends**: Month-over-month income/expense aggregation
- **Financial Health Score**: 0-100 score based on savings, budgets, stability, and balance
- **Spending Trends**: MoM and YoY growth rates
- **Cash Flow Forecast**: 3-12 month projections
- **Budget Burn Rate**: Daily consumption rate analysis
- **Spending Patterns**: Daily and weekly spending analysis
- **Category Intelligence**: Detailed category statistics
- **Transaction Statistics**: Statistical analysis with outlier detection
- **Period Comparison**: Compare two custom date ranges

### 6. Automated Data Consistency
- **Django Signals** automatically update:
  - Account balances when transactions change
  - Budget current_expense when spending occurs
- No manual data updates required
- Transaction-safe consistency guarantees

## Technology Stack

### Backend Framework
- **Django 5.2.5** - High-level Python web framework
- **Django REST Framework 3.16.1** - Powerful toolkit for building Web APIs

### Database
- **PostgreSQL 15** - Advanced open-source relational database
- **psycopg2-binary 2.9.10** - PostgreSQL adapter for Python

### Authentication
- **djangorestframework-simplejwt 5.5.1** - JSON Web Token authentication
- **PyJWT 2.10.1** - JWT implementation for Python

### AI/LLM Integration
- **LangChain 0.3.27** - Framework for developing LLM applications
- **LangChain Google GenAI 2.1.10** - Google AI integration
- **Google Gemini 2.0 Flash** - Experimental AI model for conversations
- **google-genai 1.33.0** - Google AI Python SDK

### Development Tools
- **Docker & Docker Compose** - Containerization and orchestration
- **python-dotenv 1.1.1** - Environment variable management
- **Gunicorn** - WSGI HTTP server for production

### Data & Utilities
- **numpy 2.3.2** - Numerical computing for analytics
- **Pydantic 2.11.7** - Data validation and settings management
- **httpx 0.28.1** - Modern HTTP client

## Project Architecture

### Application Structure

```
eta-api/
├── api/                          # API router and health check
├── eta_api/                      # Django project configuration
│   ├── settings/                 # Environment-specific settings
│   │   ├── base.py               # Common settings
│   │   ├── dev.py                # Development overrides
│   │   └── prod.py               # Production overrides
│   └── utils/                    # Utility functions
│       ├── responses.py          # Standardized API responses
│       └── exceptions.py         # Custom exception handlers
│
├── apps/                         # Django applications
│   ├── users/                    # User management & authentication
│   ├── accounts/                 # Financial accounts (savings, checking, etc.)
│   ├── categories/               # Income/expense categories
│   ├── transactions/             # Transaction & recurring transaction management
│   ├── budgets/                  # Budget tracking with automatic updates
│   ├── dashboard/                # Financial analytics (12+ endpoints)
│   └── chatbot/                  # AI assistant with Google Gemini
│
├── requirements.txt              # Python dependencies
├── docker-compose.yml            # Docker configuration
├── Dockerfile                    # Production Docker image
├── Dockerfile.dev                # Development Docker image
└── manage.py                     # Django management script
```

### Data Model Relationships

```
User (UUID primary key, email authentication)
├─── 1:N Accounts (savings, checking, credit, cash)
├─── 1:N Categories (income/expense with color & icon)
├─── 1:N Transactions
│    ├─── FK Account (which account the transaction belongs to)
│    ├─── FK Category (transaction category)
│    └─── Signals:
│         ├─── Auto-update Account.balance
│         └─── Auto-update Budget.current_expense
├─── 1:N RecurringTransactions (auto-process via management command)
│    ├─── FK Account
│    └─── FK Category
├─── 1:N Budgets (per-category limits)
│    └─── FK Category
└─── 1:N Conversations (chatbot)
     └─── 1:N ChatMessages (conversation history)
```

## Getting Started

### Prerequisites

- **Python 3.11+**
- **PostgreSQL 15+** (if not using Docker)
- **Docker & Docker Compose** (recommended)
- **Google Gemini API Key** (for chatbot functionality)

### Environment Setup

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd eta-api
   ```

2. **Create environment file**

   Create a `.env` file in the project root:
   ```env
   # Django Settings
   DJANGO_SETTINGS_MODULE=eta_api.settings.dev
   DJANGO_SECRET_KEY=your-secret-key-here

   # PostgreSQL Database
   POSTGRES_DB=expense_tracker
   POSTGRES_USER=expense_user
   POSTGRES_PASSWORD=password
   POSTGRES_HOST=db
   POSTGRES_PORT=5432

   # AI Configuration
   GEMINI_API_KEY=your-gemini-api-key
   ```

3. **Get Google Gemini API Key**
   - Visit [Google AI Studio](https://aistudio.google.com/app/apikey)
   - Create a new API key
   - Add it to your `.env` file

### Installation Options

#### Option 1: Docker (Recommended)

```bash
# Start all services (Django + PostgreSQL)
docker-compose up

# Run in detached mode
docker-compose up -d

# View logs
docker-compose logs -f

# Stop services
docker-compose down
```

**Services:**
- Django API: http://localhost:8000
- PostgreSQL: localhost:3000 (mapped from 5432)
- Admin panel: http://localhost:8000/admin

#### Option 2: Local Installation

```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
# Windows:
venv\Scripts\activate
# Linux/Mac:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Run migrations
python manage.py migrate

# Create superuser
python manage.py createsuperuser

# Start development server
python manage.py runserver
```

### Initial Setup

```bash
# Create database migrations
python manage.py makemigrations

# Apply migrations
python manage.py migrate

# Create admin user
python manage.py createsuperuser

# (Optional) Load sample data
python manage.py loaddata fixtures/sample_data.json
```

## API Documentation

### Base URL

```
http://localhost:8000/api/
```

### Authentication

ETA API uses **JWT (JSON Web Token)** authentication.

#### Register a New User

```http
POST /api/users/register/
Content-Type: application/json

{
  "email": "user@example.com",
  "password": "securepassword",
  "name": "John Doe"
}
```

#### Login

```http
POST /api/users/login/
Content-Type: application/json

{
  "email": "user@example.com",
  "password": "securepassword"
}
```

**Response:**
```json
{
  "success": true,
  "data": {
    "access": "eyJ0eXAiOiJKV1QiLCJhbGc...",
    "refresh": "eyJ0eXAiOiJKV1QiLCJhbGc..."
  }
}
```

#### Authenticated Requests

Include the access token in the Authorization header:

```http
Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGc...
```

### API Endpoints Overview

#### User Management
```
POST   /api/users/register/         - Register new user
POST   /api/users/login/            - Login and get JWT tokens
GET    /api/users/profile/          - Get user profile
PUT    /api/users/profile/          - Update user profile
```

#### Accounts
```
GET    /api/accounts/               - List user accounts
POST   /api/accounts/               - Create new account
GET    /api/accounts/{id}/          - Get account details
PUT    /api/accounts/{id}/          - Update account
PATCH  /api/accounts/{id}/          - Partial update account
DELETE /api/accounts/{id}/          - Delete account
```

#### Categories
```
GET    /api/categories/             - List user categories
POST   /api/categories/             - Create new category
GET    /api/categories/{id}/        - Get category details
PUT    /api/categories/{id}/        - Update category
PATCH  /api/categories/{id}/        - Partial update category
DELETE /api/categories/{id}/        - Delete category
```

#### Transactions
```
GET    /api/transactions/trans/     - List transactions
POST   /api/transactions/trans/     - Create new transaction
GET    /api/transactions/trans/{id}/ - Get transaction details
PUT    /api/transactions/trans/{id}/ - Update transaction
PATCH  /api/transactions/trans/{id}/ - Partial update transaction
DELETE /api/transactions/trans/{id}/ - Delete transaction
```

#### Recurring Transactions
```
GET    /api/transactions/recurring/     - List recurring transactions
POST   /api/transactions/recurring/     - Create recurring transaction
GET    /api/transactions/recurring/{id}/ - Get details
PUT    /api/transactions/recurring/{id}/ - Update recurring transaction
DELETE /api/transactions/recurring/{id}/ - Delete recurring transaction
```

#### Budgets
```
GET    /api/budgets/                - List user budgets
POST   /api/budgets/                - Create new budget
GET    /api/budgets/{id}/           - Get budget details
PUT    /api/budgets/{id}/           - Update budget
PATCH  /api/budgets/{id}/           - Partial update budget
DELETE /api/budgets/{id}/           - Delete budget
```

#### Dashboard Analytics
```
GET    /api/dashboard/summary/                - Overall financial summary
GET    /api/dashboard/category-breakdown/     - Spending by category
GET    /api/dashboard/budget-vs-actual/       - Budget comparison
GET    /api/dashboard/monthly-trend/          - Monthly income/expense trends
GET    /api/dashboard/financial-health/       - Financial health score (0-100)
GET    /api/dashboard/spending-trends/        - MoM and YoY growth rates
GET    /api/dashboard/cash-flow-forecast/     - Future projections (3-12 months)
GET    /api/dashboard/budget-burn-rate/       - Budget consumption analysis
GET    /api/dashboard/spending-patterns/      - Daily/weekly spending patterns
GET    /api/dashboard/category-intelligence/  - Category statistics & insights
GET    /api/dashboard/transaction-statistics/ - Statistical analysis with outliers
GET    /api/dashboard/period-comparison/      - Compare two time periods
```

#### AI Chatbot
```
POST   /api/ai/chat/                    - Send message to chatbot
GET    /api/ai/conversations/           - List user conversations
POST   /api/ai/conversations/create/    - Create new conversation
GET    /api/ai/conversations/{id}/      - Get conversation with messages
DELETE /api/ai/conversations/{id}/delete/ - Delete conversation
```

### Response Format

#### Success Response
```json
{
  "success": true,
  "message": "Request successful",
  "data": {
    // Response data
  },
  "errors": null,
  "meta": {
    // Optional metadata (pagination, etc.)
  }
}
```

#### Error Response
```json
{
  "success": false,
  "message": "Error message",
  "data": null,
  "errors": {
    "field": ["Error description"]
  },
  "status_code": 400
}
```

### Example API Requests

#### Create an Account

```bash
curl -X POST http://localhost:8000/api/accounts/ \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Savings Account",
    "account_type": "savings",
    "balance": 5000.00
  }'
```

#### Create a Transaction

```bash
curl -X POST http://localhost:8000/api/transactions/trans/ \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "account": "account-uuid-here",
    "category": "category-uuid-here",
    "type": "expense",
    "amount": 50.00,
    "description": "Grocery shopping",
    "date": "2025-10-30"
  }'
```

#### Chat with AI Assistant

```bash
curl -X POST http://localhost:8000/api/ai/chat/ \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "message": "What is my total spending this month?",
    "conversation_id": "optional-conversation-uuid"
  }'
```

#### Get Financial Health Score

```bash
curl -X GET http://localhost:8000/api/dashboard/financial-health/ \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN"
```

## Database Schema

### User Model
- **Primary Key**: UUID (not integer)
- **Authentication**: Email-based (not username)
- **Fields**: id, email, name, password (hashed), created_at, last_login, chatbot_enabled, ai_insights_enabled

### Account Model
- **Fields**: id, user, name, account_type (savings/current/credit/cash/other), balance, created_at
- **Auto-Updated**: Balance is automatically maintained via Django signals

### Category Model
- **Fields**: id, user, name, type (income/expense), colorHex, icon, created_at
- **UI Customization**: Supports custom colors and icons

### Transaction Model
- **Fields**: id, user, account, category, type (income/expense), amount, description, date, created_at
- **Signals**: Automatically updates Account.balance and Budget.current_expense

### RecurringTransaction Model
- **Fields**: id, user, account, category, type, amount, description, frequency (daily/weekly/monthly/yearly), start_date, end_date, last_processed_date
- **Processing**: Via management command `process_recurring_transactions`

### Budget Model
- **Fields**: id, user, category, amount (limit), current_expense (auto-calculated), start_date, end_date, created_at
- **Properties**: `remaining` = amount - current_expense
- **Auto-Updated**: current_expense via Django signals

### Conversation & ChatMessage Models
- **Conversation**: id, user, title (auto-generated), created_at, updated_at
- **ChatMessage**: id, conversation, role (user/assistant/system), content, created_at
- **Ordering**: Messages ordered by created_at, conversations by -updated_at

## AI Chatbot

### Overview

The ETA API chatbot is powered by **Google Gemini 2.0 Flash** via **LangChain**, providing natural language financial insights and query capabilities.

### Available Tools (9 Total)

1. **expense_tool** - Total expenses for current month
2. **income_tool** - Total income for current month
3. **category_breakdown_tool** - Expense breakdown by category
4. **biggest_expense_tool** - Largest single expense
5. **budget_status_tool** - Active budget status and alerts
6. **recent_transactions_tool** - Last 10 transactions
7. **account_balances_tool** - All account balances and total
8. **spending_trends_tool** - Month-over-month comparison
9. **top_spending_category_tool** - Highest spending category

### How It Works

1. User sends a message via `/api/ai/chat/`
2. System loads conversation context (last 10 messages)
3. LangChain agent analyzes the query
4. Agent automatically selects and calls relevant tools
5. Tools fetch data from Django ORM
6. AI generates natural language response
7. Response saved to database and returned to user

### Example Conversations

**Query:** "How much did I spend this month?"
**Response:** Uses `expense_tool` to fetch current month expenses and returns formatted answer.

**Query:** "What's my biggest expense?"
**Response:** Uses `biggest_expense_tool` to find the largest transaction.

**Query:** "Am I staying within my budgets?"
**Response:** Uses `budget_status_tool` to analyze budget adherence and provides insights.

**Query:** "Show me my account balances"
**Response:** Uses `account_balances_tool` to list all accounts and total balance.

### Configuration

**Model**: Google Gemini 2.0 Flash Experimental
**Temperature**: 0.7 (balanced creativity and accuracy)
**Max Iterations**: 5 tool calls per query
**Context**: Last 10 messages for multi-turn conversations

## Dashboard Analytics

### Financial Health Score

A comprehensive **0-100 score** based on:
- **Savings Rate (40 points)**: Income vs. expense ratio
- **Budget Adherence (30 points)**: Staying within budgets
- **Spending Stability (20 points)**: Consistency in spending patterns
- **Account Balance Health (10 points)**: Overall balance status

**Rating Levels**:
- 80-100: Excellent
- 60-79: Good
- 40-59: Fair
- 0-39: Needs Improvement

### Spending Trends

- **Month-over-Month (MoM)**: Compare current month to previous month
- **Year-over-Year (YoY)**: Compare current month to same month last year
- **Growth Rates**: Percentage change in spending

### Cash Flow Forecast

- Projects income and expenses for **1-12 months** ahead
- Based on historical averages
- Calculates projected net balance
- Helps with financial planning

### Budget Burn Rate

- **Daily consumption rate** of budget
- **Days until exhaustion** prediction
- **Over-budget alerts** for exceeded categories
- Helps prevent overspending

### Spending Patterns

- **Daily patterns**: Spending by day of week
- **Weekly patterns**: Weekly aggregation
- Identifies high-spending days
- Helps optimize spending behavior

### Category Intelligence

- Per-category statistics
- Percentage of total spending
- Average transaction amounts
- Transaction counts and trends

### Transaction Statistics

- Statistical analysis (mean, median, std deviation)
- **Outlier detection**: Identifies unusual transactions (>2 std deviations)
- Recent transaction summary
- Data-driven insights

### Period Comparison

- Compare any two custom date ranges
- Side-by-side income/expense comparison
- Percentage changes
- Trend analysis

## Automated Systems

### Django Signals (Automatic Data Updates)

**Location**: `apps/transactions/signals.py`

#### Account Balance Auto-Update
- **Trigger**: Transaction create/update/delete
- **Action**: Automatically adjusts Account.balance
- **Logic**:
  - Income: `balance += amount`
  - Expense: `balance -= amount`
  - Update: Revert old amount, apply new amount

#### Budget Expense Auto-Update
- **Trigger**: Transaction create/update/delete
- **Action**: Recalculates Budget.current_expense
- **Scope**: Only expense transactions within budget date range
- **Smart**: Handles category and date changes properly

**IMPORTANT**: Never manually update `Budget.current_expense` or `Account.balance` - they are managed by signals!

### Recurring Transaction Processing

**Command**: `python manage.py process_recurring_transactions`

**What It Does**:
1. Finds active recurring transactions (within start/end date range)
2. Creates actual Transaction records based on frequency
3. Updates `last_processed_date` to prevent duplicates
4. Respects transaction type (income or expense)

**Frequency Options**:
- **Daily**: Creates transaction every day
- **Weekly**: Creates transaction every 7 days
- **Monthly**: Creates transaction on same day each month
- **Yearly**: Creates transaction on same day each year

**Scheduling in Production**:

**Linux/Mac (crontab)**:
```bash
# Run daily at midnight
0 0 * * * /path/to/python /path/to/manage.py process_recurring_transactions
```

**Windows (Task Scheduler)**:
1. Open Task Scheduler
2. Create Basic Task
3. Set trigger: Daily at midnight
4. Action: Start a program
5. Program: `python.exe`
6. Arguments: `manage.py process_recurring_transactions`
7. Start in: Project directory

**Docker (docker-compose)**:
```yaml
services:
  scheduler:
    image: eta-api:latest
    command: sh -c "while true; do python manage.py process_recurring_transactions && sleep 86400; done"
```

**Celery Beat** (recommended for production):
```python
# celerybeat-schedule.py
CELERY_BEAT_SCHEDULE = {
    'process-recurring-transactions': {
        'task': 'apps.transactions.tasks.process_recurring',
        'schedule': crontab(hour=0, minute=0),  # Daily at midnight
    },
}
```

## Development

### Project Structure Explained

```
apps/
├── users/              - User model, authentication, registration
├── accounts/           - Financial account management
├── categories/         - Income/expense category definitions
├── transactions/       - Transaction CRUD + signals + management commands
├── budgets/            - Budget tracking with auto-updates
├── dashboard/          - Analytics views and calculation functions
└── chatbot/            - AI assistant with LangChain integration
```

### Common Development Commands

```bash
# Database operations
python manage.py makemigrations          # Create migrations
python manage.py migrate                 # Apply migrations
python manage.py showmigrations          # Show migration status

# User management
python manage.py createsuperuser         # Create admin user
python manage.py changepassword <email>  # Change user password

# Development server
python manage.py runserver               # Start dev server (port 8000)
python manage.py runserver 0.0.0.0:9000  # Custom host/port

# Django shell
python manage.py shell                   # Interactive Python shell
python manage.py dbshell                 # Database shell

# Testing
python manage.py test                    # Run all tests
python manage.py test apps.users         # Run specific app tests

# Static files
python manage.py collectstatic           # Collect static files

# Data management
python manage.py dumpdata > backup.json  # Backup database
python manage.py loaddata backup.json    # Restore database

# Process recurring transactions
python manage.py process_recurring_transactions
python manage.py process_recurring_transactions --dry-run

# Check for issues
python manage.py check                   # Check for problems
python manage.py check --deploy          # Deployment checks
```

### Settings Configuration

**Settings Hierarchy**:
1. `eta_api/settings/base.py` - Common settings for all environments
2. `eta_api/settings/dev.py` - Development-specific settings
3. `eta_api/settings/prod.py` - Production-specific settings

**Select Settings Module**:
```bash
# Via environment variable
export DJANGO_SETTINGS_MODULE=eta_api.settings.prod

# Via .env file
DJANGO_SETTINGS_MODULE=eta_api.settings.dev

# Via command line
python manage.py runserver --settings=eta_api.settings.prod
```

### Adding New Features

#### 1. Create a New Django App

```bash
python manage.py startapp apps/feature_name
```

#### 2. Register in Settings

```python
# eta_api/settings/base.py
INSTALLED_APPS = [
    # ...
    'apps.feature_name',
]
```

#### 3. Create Models

```python
# apps/feature_name/models.py
from django.db import models
from django.conf import settings

class MyModel(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    # ... other fields

    class Meta:
        ordering = ['-created_at']
```

#### 4. Create Serializers

```python
# apps/feature_name/serializers.py
from rest_framework import serializers
from .models import MyModel

class MyModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = MyModel
        fields = '__all__'
        read_only_fields = ['user']
```

#### 5. Create Views

```python
# apps/feature_name/views.py
from rest_framework import viewsets, permissions
from .models import MyModel
from .serializers import MyModelSerializer

class MyModelViewSet(viewsets.ModelViewSet):
    serializer_class = MyModelSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return MyModel.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
```

#### 6. Register URLs

```python
# apps/feature_name/urls.py
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import MyModelViewSet

router = DefaultRouter()
router.register(r'items', MyModelViewSet, basename='item')

urlpatterns = [
    path('', include(router.urls)),
]

# api/urls.py
urlpatterns = [
    # ...
    path('feature/', include('apps.feature_name.urls')),
]
```

#### 7. Create and Apply Migrations

```bash
python manage.py makemigrations
python manage.py migrate
```

### Testing

Create test files in each app:

```python
# apps/feature_name/tests.py
from rest_framework.test import APITestCase
from rest_framework import status
from apps.users.models import User

class MyFeatureTestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            email='test@example.com',
            password='testpass123'
        )
        self.client.force_authenticate(user=self.user)

    def test_create_item(self):
        response = self.client.post('/api/feature/items/', {
            'name': 'Test Item'
        })
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
```

Run tests:
```bash
python manage.py test
python manage.py test apps.feature_name
python manage.py test apps.feature_name.tests.MyFeatureTestCase
```

## Deployment

### Production Checklist

- [ ] Set `DEBUG = False` in production settings
- [ ] Configure `ALLOWED_HOSTS` with your domain
- [ ] Use strong `SECRET_KEY` (generate new one)
- [ ] Set up PostgreSQL database
- [ ] Configure environment variables in `.env`
- [ ] Set up static file serving (nginx + collectstatic)
- [ ] Configure HTTPS/SSL certificates
- [ ] Set up logging and monitoring
- [ ] Configure CORS settings if needed
- [ ] Set up automated backups
- [ ] Schedule recurring transaction processing (cron/celery)
- [ ] Configure email backend for notifications
- [ ] Set up Sentry or error tracking
- [ ] Enable database connection pooling
- [ ] Configure caching (Redis)

### Docker Production Deployment

```bash
# Build production image
docker build -t eta-api:latest .

# Run with docker-compose
docker-compose -f docker-compose.prod.yml up -d

# Apply migrations
docker-compose exec web python manage.py migrate

# Collect static files
docker-compose exec web python manage.py collectstatic --noinput

# Create superuser
docker-compose exec web python manage.py createsuperuser
```

### Environment Variables for Production

```env
DJANGO_SETTINGS_MODULE=eta_api.settings.prod
DJANGO_SECRET_KEY=your-production-secret-key
DEBUG=False
ALLOWED_HOSTS=yourdomain.com,www.yourdomain.com

POSTGRES_DB=expense_tracker
POSTGRES_USER=expense_user
POSTGRES_PASSWORD=strong-production-password
POSTGRES_HOST=db
POSTGRES_PORT=5432

GEMINI_API_KEY=your-gemini-api-key

# Optional
REDIS_URL=redis://redis:6379
SENTRY_DSN=your-sentry-dsn
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_HOST_USER=your-email@example.com
EMAIL_HOST_PASSWORD=your-email-password
```

### Gunicorn Configuration

```python
# gunicorn.conf.py
bind = "0.0.0.0:8000"
workers = 4
worker_class = "sync"
worker_connections = 1000
max_requests = 1000
max_requests_jitter = 100
timeout = 30
keepalive = 2
```

### Nginx Configuration

```nginx
server {
    listen 80;
    server_name yourdomain.com;

    location /static/ {
        alias /app/staticfiles/;
    }

    location /media/ {
        alias /app/media/;
    }

    location / {
        proxy_pass http://web:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

## Contributing

We welcome contributions! Please follow these guidelines:

### How to Contribute

1. **Fork the repository**
2. **Create a feature branch**: `git checkout -b feature/your-feature-name`
3. **Make your changes**
4. **Write tests** for new features
5. **Ensure all tests pass**: `python manage.py test`
6. **Commit your changes**: `git commit -m "Add feature: description"`
7. **Push to your fork**: `git push origin feature/your-feature-name`
8. **Create a Pull Request**

### Code Style

- Follow **PEP 8** style guide for Python code
- Use meaningful variable and function names
- Add docstrings to classes and functions
- Keep functions small and focused
- Write unit tests for new features
- Use Django best practices

### Commit Message Format

```
feat: Add new analytics endpoint for spending patterns
fix: Correct budget calculation in signals
docs: Update README with deployment instructions
test: Add tests for transaction signals
refactor: Simplify category breakdown calculation
```

### Pull Request Guidelines

- Provide clear description of changes
- Reference related issues
- Include screenshots for UI changes
- Ensure all tests pass
- Update documentation if needed

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Support

- **Documentation**: Check [CLAUDE.md](CLAUDE.md) for developer guidance
- **Issues**: Report bugs via [GitHub Issues](<repository-url>/issues)
- **Questions**: Open a discussion on [GitHub Discussions](<repository-url>/discussions)

## Acknowledgments

- **Django** - The web framework for perfectionists with deadlines
- **Django REST Framework** - Powerful and flexible toolkit for building Web APIs
- **Google Gemini** - AI model powering the chatbot
- **LangChain** - Framework for LLM application development
- **PostgreSQL** - The world's most advanced open source database

---

**Built with Django REST Framework and Google Gemini**

For detailed developer documentation, see [CLAUDE.md](CLAUDE.md).
