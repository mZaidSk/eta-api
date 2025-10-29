# Dashboard API - Complete Guide

## Overview

The ETA API Dashboard provides comprehensive financial analytics and insights. It includes both basic and advanced analytics endpoints to help users understand their financial health, spending patterns, and future projections.

**Base URL:** `/api/dashboard/`

**Authentication:** All endpoints require JWT authentication

---

## Table of Contents

1. [Basic Analytics](#basic-analytics)
2. [Advanced Analytics](#advanced-analytics)
3. [Query Parameters](#query-parameters)
4. [Response Format](#response-format)
5. [Use Cases](#use-cases)

---

## Basic Analytics

### 1. Dashboard Summary

**Endpoint:** `GET /api/dashboard/summary/`

**Description:** Get overview of total income, expenses, net balance, and account details

**Query Parameters:**
- `account` (optional): Filter by specific account ID

**Response:**
```json
{
  "success": true,
  "message": "Dashboard summary fetched successfully",
  "data": {
    "total_income": 5000.00,
    "total_expense": 3200.50,
    "net_balance": 1799.50,
    "accounts": [
      {
        "id": 1,
        "name": "Savings Account",
        "balance": 10000.00
      },
      {
        "id": 2,
        "name": "Checking Account",
        "balance": 2500.00
      }
    ]
  }
}
```

---

### 2. Category Breakdown

**Endpoint:** `GET /api/dashboard/category-breakdown/`

**Description:** Get income and expense breakdown by category

**Query Parameters:**
- `account` (optional): Filter by specific account ID

**Response:**
```json
{
  "success": true,
  "message": "Category breakdown fetched successfully",
  "data": {
    "income": [
      {
        "category": "Salary",
        "total": 5000.00
      }
    ],
    "expense": [
      {
        "category": "Food",
        "total": 800.00
      },
      {
        "category": "Transport",
        "total": 400.00
      },
      {
        "category": "Entertainment",
        "total": 300.00
      }
    ]
  }
}
```

---

### 3. Budget vs Actual

**Endpoint:** `GET /api/dashboard/budget-vs-actual/`

**Description:** Compare budgeted amounts vs actual spending per category

**Query Parameters:**
- `account` (optional): Filter by specific account ID

**Response:**
```json
{
  "success": true,
  "message": "Budget vs Actual fetched successfully",
  "data": [
    {
      "category": "Food",
      "budget": 1000.00,
      "actual": 800.00,
      "remaining": 200.00
    },
    {
      "category": "Transport",
      "budget": 500.00,
      "actual": 550.00,
      "remaining": -50.00
    }
  ]
}
```

---

### 4. Monthly Trend

**Endpoint:** `GET /api/dashboard/monthly-trend/`

**Description:** Get month-by-month income and expense trends

**Query Parameters:**
- `account` (optional): Filter by specific account ID

**Response:**
```json
{
  "success": true,
  "message": "Monthly trend fetched successfully",
  "data": [
    {
      "month": "2025-08",
      "income": 5000.00,
      "expense": 3100.00
    },
    {
      "month": "2025-09",
      "income": 5200.00,
      "expense": 3300.00
    },
    {
      "month": "2025-10",
      "income": 5000.00,
      "expense": 3200.50
    }
  ]
}
```

---

## Advanced Analytics

### 5. Financial Health Score

**Endpoint:** `GET /api/dashboard/financial-health/`

**Description:** Calculate comprehensive financial health score (0-100) based on:
- Savings rate (40 points)
- Budget adherence (30 points)
- Spending stability (20 points)
- Account balance health (10 points)

**Response:**
```json
{
  "success": true,
  "message": "Financial health score calculated successfully",
  "data": {
    "total_score": 72.5,
    "rating": "Good",
    "savings_rate": 36.0,
    "savings_points": 32.0,
    "budget_adherence": 75.0,
    "budget_points": 22.5,
    "spending_stability": 85.0,
    "stability_points": 17.0,
    "total_balance": 12500.00,
    "balance_points": 10.0
  }
}
```

**Rating Scale:**
- 80-100: Excellent
- 60-79: Good
- 40-59: Fair
- 20-39: Needs Improvement
- 0-19: Critical

---

### 6. Spending Trends & Growth Rates

**Endpoint:** `GET /api/dashboard/spending-trends/`

**Description:** Get month-over-month and year-over-year spending growth rates

**Query Parameters:**
- `account` (optional): Filter by specific account ID

**Response:**
```json
{
  "success": true,
  "message": "Spending trends fetched successfully",
  "data": {
    "current_month": 3200.50,
    "last_month": 3100.00,
    "mom_growth_rate": 3.24,
    "last_year_same_month": 2800.00,
    "yoy_growth_rate": 14.30,
    "trend": "increasing"
  }
}
```

**Trend Values:**
- `increasing`: Spending is going up
- `decreasing`: Spending is going down
- `stable`: No significant change

---

### 7. Cash Flow Forecast

**Endpoint:** `GET /api/dashboard/cash-flow-forecast/`

**Description:** Predict future cash flow based on historical averages (last 6 months)

**Query Parameters:**
- `months` (optional): Number of months to forecast (default: 3, max: 12)

**Response:**
```json
{
  "success": true,
  "message": "Cash flow forecast generated successfully",
  "data": {
    "current_balance": 12500.00,
    "avg_monthly_income": 5066.67,
    "avg_monthly_expense": 3166.67,
    "forecasts": [
      {
        "month": "2025-11",
        "projected_income": 5066.67,
        "projected_expense": 3166.67,
        "projected_net": 1900.00,
        "projected_balance": 14400.00
      },
      {
        "month": "2025-12",
        "projected_income": 5066.67,
        "projected_expense": 3166.67,
        "projected_net": 1900.00,
        "projected_balance": 16300.00
      },
      {
        "month": "2026-01",
        "projected_income": 5066.67,
        "projected_expense": 3166.67,
        "projected_net": 1900.00,
        "projected_balance": 18200.00
      }
    ]
  }
}
```

---

### 8. Budget Burn Rate

**Endpoint:** `GET /api/dashboard/budget-burn-rate/`

**Description:** Analyze how fast budgets are being consumed and predict exhaustion dates

**Response:**
```json
{
  "success": true,
  "message": "Budget burn rate calculated successfully",
  "data": [
    {
      "category": "Food",
      "budget_amount": 1000.00,
      "current_expense": 600.00,
      "daily_burn_rate": 30.00,
      "projected_total": 900.00,
      "days_elapsed": 20,
      "days_remaining": 10,
      "days_to_exhaust": 13,
      "percent_used": 60.0,
      "percent_time_elapsed": 66.67,
      "status": "on_track"
    },
    {
      "category": "Entertainment",
      "budget_amount": 500.00,
      "current_expense": 480.00,
      "daily_burn_rate": 24.00,
      "projected_total": 720.00,
      "days_elapsed": 20,
      "days_remaining": 10,
      "days_to_exhaust": 1,
      "percent_used": 96.0,
      "percent_time_elapsed": 66.67,
      "status": "overspending"
    }
  ]
}
```

**Status Values:**
- `on_track`: Spending is healthy
- `on_track_high`: Spending slightly above pace but within budget
- `overspending`: Spending significantly faster than budget allows

---

### 9. Spending Patterns

**Endpoint:** `GET /api/dashboard/spending-patterns/`

**Description:** Analyze spending patterns by day of week and weekly trends (last 90 days)

**Query Parameters:**
- `account` (optional): Filter by specific account ID

**Response:**
```json
{
  "success": true,
  "message": "Spending patterns analyzed successfully",
  "data": {
    "daily_pattern": [
      {
        "day": "Monday",
        "avg_spending": 145.50,
        "transaction_count": 12
      },
      {
        "day": "Tuesday",
        "avg_spending": 120.30,
        "transaction_count": 11
      },
      {
        "day": "Wednesday",
        "avg_spending": 135.00,
        "transaction_count": 13
      },
      {
        "day": "Thursday",
        "avg_spending": 110.25,
        "transaction_count": 10
      },
      {
        "day": "Friday",
        "avg_spending": 180.75,
        "transaction_count": 15
      },
      {
        "day": "Saturday",
        "avg_spending": 220.00,
        "transaction_count": 13
      },
      {
        "day": "Sunday",
        "avg_spending": 95.50,
        "transaction_count": 8
      }
    ],
    "weekly_pattern": [
      {
        "week_start": "2025-08-04",
        "total_spending": 750.50,
        "transaction_count": 25
      },
      {
        "week_start": "2025-08-11",
        "total_spending": 820.30,
        "transaction_count": 28
      }
    ]
  }
}
```

---

### 10. Category Intelligence

**Endpoint:** `GET /api/dashboard/category-intelligence/`

**Description:** Detailed category-wise spending analysis with statistics

**Query Parameters:**
- `account` (optional): Filter by specific account ID

**Response:**
```json
{
  "success": true,
  "message": "Category intelligence fetched successfully",
  "data": {
    "total_spending": 3200.50,
    "category_count": 5,
    "categories": [
      {
        "category": "Food",
        "total_spent": 800.00,
        "percentage_of_total": 25.0,
        "transaction_count": 15,
        "average_transaction": 53.33,
        "largest_transaction": 150.00,
        "smallest_transaction": 12.50
      },
      {
        "category": "Transport",
        "total_spent": 550.00,
        "percentage_of_total": 17.19,
        "transaction_count": 8,
        "average_transaction": 68.75,
        "largest_transaction": 120.00,
        "smallest_transaction": 25.00
      }
    ]
  }
}
```

---

### 11. Transaction Statistics & Outliers

**Endpoint:** `GET /api/dashboard/transaction-statistics/`

**Description:** Statistical analysis with outlier detection (transactions > 2 std deviations from mean)

**Query Parameters:**
- `account` (optional): Filter by specific account ID
- `days` (optional): Analysis period in days (default: 30, max: 365)

**Response:**
```json
{
  "success": true,
  "message": "Transaction statistics calculated successfully",
  "data": {
    "period_days": 30,
    "income": {
      "total": 5000.00,
      "count": 2,
      "average": 2500.00,
      "largest": 3000.00,
      "smallest": 2000.00
    },
    "expense": {
      "total": 3200.50,
      "count": 45,
      "average": 71.12,
      "largest": 450.00,
      "smallest": 12.50,
      "std_deviation": 85.30
    },
    "outliers": [
      {
        "date": "2025-10-15",
        "amount": 450.00,
        "category": "Electronics",
        "description": "New laptop purchase"
      },
      {
        "date": "2025-10-20",
        "amount": 380.00,
        "category": "Entertainment",
        "description": "Concert tickets"
      }
    ],
    "daily_average_expense": 106.68
  }
}
```

---

### 12. Period Comparison

**Endpoint:** `GET /api/dashboard/period-comparison/`

**Description:** Compare spending/income between two custom date periods

**Query Parameters (Required):**
- `period1_start`: Start date for period 1 (format: YYYY-MM-DD)
- `period1_end`: End date for period 1 (format: YYYY-MM-DD)
- `period2_start`: Start date for period 2 (format: YYYY-MM-DD)
- `period2_end`: End date for period 2 (format: YYYY-MM-DD)
- `account` (optional): Filter by specific account ID

**Example:**
```
GET /api/dashboard/period-comparison/?period1_start=2025-08-01&period1_end=2025-08-31&period2_start=2025-09-01&period2_end=2025-09-30
```

**Response:**
```json
{
  "success": true,
  "message": "Period comparison completed successfully",
  "data": {
    "period1": {
      "start_date": "2025-08-01",
      "end_date": "2025-08-31",
      "income": 5000.00,
      "expense": 3100.00,
      "net": 1900.00
    },
    "period2": {
      "start_date": "2025-09-01",
      "end_date": "2025-09-30",
      "income": 5200.00,
      "expense": 3300.00,
      "net": 1900.00
    },
    "comparison": {
      "income_difference": 200.00,
      "income_change_percent": 4.0,
      "expense_difference": 200.00,
      "expense_change_percent": 6.45
    }
  }
}
```

---

## Query Parameters

### Common Parameters

All dashboard endpoints support the following query parameters:

| Parameter | Type | Description | Default |
|-----------|------|-------------|---------|
| `account` | integer | Filter data by specific account ID | All accounts |

### Endpoint-Specific Parameters

| Endpoint | Parameter | Type | Description | Default |
|----------|-----------|------|-------------|---------|
| Cash Flow Forecast | `months` | integer | Months to forecast ahead (max 12) | 3 |
| Transaction Statistics | `days` | integer | Analysis period in days (max 365) | 30 |
| Period Comparison | `period1_start` | date | Start date for period 1 (YYYY-MM-DD) | Required |
| Period Comparison | `period1_end` | date | End date for period 1 (YYYY-MM-DD) | Required |
| Period Comparison | `period2_start` | date | Start date for period 2 (YYYY-MM-DD) | Required |
| Period Comparison | `period2_end` | date | End date for period 2 (YYYY-MM-DD) | Required |

---

## Response Format

All endpoints follow the standard response format:

### Success Response
```json
{
  "success": true,
  "message": "Descriptive success message",
  "data": { ... },
  "errors": null
}
```

### Error Response
```json
{
  "success": false,
  "message": "Error description",
  "data": null,
  "errors": { ... }
}
```

---

## Use Cases

### 1. Financial Health Dashboard

**Goal:** Show user's overall financial health at a glance

**Endpoints to use:**
- `/api/dashboard/summary/` - Get overview
- `/api/dashboard/financial-health/` - Get health score
- `/api/dashboard/budget-vs-actual/` - Check budget status

**Implementation:**
```javascript
// Fetch dashboard overview
const summary = await fetch('/api/dashboard/summary/');
const health = await fetch('/api/dashboard/financial-health/');
const budgets = await fetch('/api/dashboard/budget-vs-actual/');

// Display:
// - Total balance
// - Health score with rating
// - Budget alerts if over-spending
```

---

### 2. Spending Insights Page

**Goal:** Help users understand their spending patterns

**Endpoints to use:**
- `/api/dashboard/category-intelligence/` - Category breakdown with stats
- `/api/dashboard/spending-patterns/` - Day/week patterns
- `/api/dashboard/spending-trends/` - Growth rates

**Implementation:**
```javascript
// Get detailed spending analysis
const categoryInsights = await fetch('/api/dashboard/category-intelligence/');
const patterns = await fetch('/api/dashboard/spending-patterns/');
const trends = await fetch('/api/dashboard/spending-trends/');

// Display:
// - Pie chart of spending by category
// - Bar chart of spending by day of week
// - Trend indicators (up/down arrows)
```

---

### 3. Budget Management

**Goal:** Monitor budget performance and predict issues

**Endpoints to use:**
- `/api/dashboard/budget-vs-actual/` - Current status
- `/api/dashboard/budget-burn-rate/` - Consumption rate
- `/api/dashboard/transaction-statistics/` - Outlier detection

**Implementation:**
```javascript
// Monitor budgets
const budgetStatus = await fetch('/api/dashboard/budget-vs-actual/');
const burnRates = await fetch('/api/dashboard/budget-burn-rate/');

// Alert if:
// - Any budget is over 80% consumed
// - Burn rate indicates early exhaustion
// - Status is "overspending"
```

---

### 4. Financial Planning

**Goal:** Help users plan future finances

**Endpoints to use:**
- `/api/dashboard/cash-flow-forecast/?months=6` - 6-month projection
- `/api/dashboard/monthly-trend/` - Historical trends
- `/api/dashboard/period-comparison/` - Compare periods

**Implementation:**
```javascript
// Get forecast
const forecast = await fetch('/api/dashboard/cash-flow-forecast/?months=6');
const trends = await fetch('/api/dashboard/monthly-trend/');

// Display:
// - Line chart of projected balance
// - Recommendation based on trends
// - Savings goals progress
```

---

### 5. Expense Analysis Report

**Goal:** Generate comprehensive expense report

**Endpoints to use:**
- `/api/dashboard/transaction-statistics/?days=90` - 90-day stats
- `/api/dashboard/category-intelligence/` - Category details
- `/api/dashboard/spending-patterns/` - Behavioral patterns

**Implementation:**
```javascript
// Generate report
const stats = await fetch('/api/dashboard/transaction-statistics/?days=90');
const categories = await fetch('/api/dashboard/category-intelligence/');
const patterns = await fetch('/api/dashboard/spending-patterns/');

// Export to PDF with:
// - Total spending
// - Top categories
// - Unusual transactions (outliers)
// - Peak spending days
```

---

## Performance Tips

1. **Use account filtering** when possible to reduce data processing
2. **Cache forecast data** as it's computationally expensive
3. **Limit date ranges** in period comparisons to reasonable periods
4. **Paginate transaction lists** in your frontend

---

## Example Integration (JavaScript/TypeScript)

```typescript
// Dashboard API Service
class DashboardService {
  private baseUrl = '/api/dashboard/';
  private headers = {
    'Authorization': `Bearer ${getToken()}`,
    'Content-Type': 'application/json'
  };

  async getFinancialHealth() {
    const response = await fetch(`${this.baseUrl}financial-health/`, {
      headers: this.headers
    });
    return response.json();
  }

  async getCashFlowForecast(months: number = 3) {
    const response = await fetch(
      `${this.baseUrl}cash-flow-forecast/?months=${months}`,
      { headers: this.headers }
    );
    return response.json();
  }

  async getSpendingPatterns(accountId?: number) {
    const url = accountId
      ? `${this.baseUrl}spending-patterns/?account=${accountId}`
      : `${this.baseUrl}spending-patterns/`;

    const response = await fetch(url, { headers: this.headers });
    return response.json();
  }

  async comparePeriods(
    period1Start: string,
    period1End: string,
    period2Start: string,
    period2End: string
  ) {
    const params = new URLSearchParams({
      period1_start: period1Start,
      period1_end: period1End,
      period2_start: period2Start,
      period2_end: period2End
    });

    const response = await fetch(
      `${this.baseUrl}period-comparison/?${params}`,
      { headers: this.headers }
    );
    return response.json();
  }
}

// Usage
const dashboard = new DashboardService();

// Load financial health
const health = await dashboard.getFinancialHealth();
console.log(`Health Score: ${health.data.total_score}`);

// Get 6-month forecast
const forecast = await dashboard.getCashFlowForecast(6);
console.log('Projected balances:', forecast.data.forecasts);

// Compare last two months
const today = new Date();
const thisMonthStart = new Date(today.getFullYear(), today.getMonth(), 1);
const thisMonthEnd = new Date(today.getFullYear(), today.getMonth() + 1, 0);
const lastMonthStart = new Date(today.getFullYear(), today.getMonth() - 1, 1);
const lastMonthEnd = new Date(today.getFullYear(), today.getMonth(), 0);

const comparison = await dashboard.comparePeriods(
  formatDate(lastMonthStart),
  formatDate(lastMonthEnd),
  formatDate(thisMonthStart),
  formatDate(thisMonthEnd)
);
console.log('Expense change:', comparison.data.comparison.expense_change_percent);
```

---

## Support

For issues, questions, or feature requests, please contact the development team or check the main project documentation.

---

## Changelog

**Version 2.0** - Advanced Analytics Update
- Added Financial Health Score
- Added Spending Trends & Growth Rates
- Added Cash Flow Forecasting
- Added Budget Burn Rate Analysis
- Added Spending Pattern Detection
- Added Category Intelligence
- Added Transaction Statistics with Outlier Detection
- Added Period Comparison

**Version 1.0** - Initial Release
- Basic dashboard summary
- Category breakdown
- Budget vs Actual
- Monthly trends
