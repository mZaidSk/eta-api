from uuid import UUID
from apps.users.models import User
from langchain.tools import tool
from .tools import (
    get_total_expense_this_month,
    get_total_income_this_month,
    get_category_breakdown,
    get_biggest_expense,
    get_budget_status,
    get_recent_transactions,
    get_account_balances,
    get_spending_trends,
    get_top_spending_category,
)


@tool
def expense_tool(user_id: str) -> str:
    """Use this to get the user's total expense for the current month."""
    clean_id = user_id.strip().replace("'", "").replace('"', "").replace(".", "")
    user = User.objects.get(id=UUID(clean_id))
    return get_total_expense_this_month(user)


@tool
def income_tool(user_id: str) -> str:
    """Use this to get the user's total income for the current month."""
    clean_id = user_id.strip().replace("'", "").replace('"', "").replace(".", "")
    user = User.objects.get(id=UUID(clean_id))
    return get_total_income_this_month(user)


@tool
def category_breakdown_tool(user_id: str) -> str:
    """Use this to get a breakdown of expenses by category for the current month."""
    clean_id = user_id.strip().replace("'", "").replace('"', "").replace(".", "")
    user = User.objects.get(id=UUID(clean_id))
    return get_category_breakdown(user)


@tool
def biggest_expense_tool(user_id: str) -> str:
    """Use this to find the user's largest single expense for the current month."""
    clean_id = user_id.strip().replace("'", "").replace('"', "").replace(".", "")
    user = User.objects.get(id=UUID(clean_id))
    return get_biggest_expense(user)


@tool
def budget_status_tool(user_id: str) -> str:
    """Use this to check the status of all active budgets and see if the user is over or under budget."""
    clean_id = user_id.strip().replace("'", "").replace('"', "").replace(".", "")
    user = User.objects.get(id=UUID(clean_id))
    return get_budget_status(user)


@tool
def recent_transactions_tool(user_id: str) -> str:
    """Use this to get the user's 10 most recent transactions."""
    clean_id = user_id.strip().replace("'", "").replace('"', "").replace(".", "")
    user = User.objects.get(id=UUID(clean_id))
    return get_recent_transactions(user)


@tool
def account_balances_tool(user_id: str) -> str:
    """Use this to get the current balance of all user's accounts and the total."""
    clean_id = user_id.strip().replace("'", "").replace('"', "").replace(".", "")
    user = User.objects.get(id=UUID(clean_id))
    return get_account_balances(user)


@tool
def spending_trends_tool(user_id: str) -> str:
    """Use this to compare current month spending with last month and identify trends."""
    clean_id = user_id.strip().replace("'", "").replace('"', "").replace(".", "")
    user = User.objects.get(id=UUID(clean_id))
    return get_spending_trends(user)


@tool
def top_spending_category_tool(user_id: str) -> str:
    """Use this to find which category the user spent the most money on this month."""
    clean_id = user_id.strip().replace("'", "").replace('"', "").replace(".", "")
    user = User.objects.get(id=UUID(clean_id))
    return get_top_spending_category(user)


tools = [
    expense_tool,
    income_tool,
    category_breakdown_tool,
    biggest_expense_tool,
    budget_status_tool,
    recent_transactions_tool,
    account_balances_tool,
    spending_trends_tool,
    top_spending_category_tool,
]
