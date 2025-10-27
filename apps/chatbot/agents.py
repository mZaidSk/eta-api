from uuid import UUID
from apps.users.models import User
from langchain.tools import tool
from .tools import get_total_expense_this_month, get_total_income_this_month


@tool
def expense_tool(user_id: str) -> str:
    """Use this to get the user's total expense this month."""
    clean_id = user_id.strip().replace("'", "").replace('"', "").replace(".", "")
    user = User.objects.get(id=UUID(clean_id))
    return get_total_expense_this_month(user)


@tool
def income_tool(user_id: str) -> str:
    """Use this to get the user's total income this month."""
    clean_id = user_id.strip().replace("'", "").replace('"', "").replace(".", "")
    user = User.objects.get(id=UUID(clean_id))
    return get_total_income_this_month(user)


tools = [expense_tool, income_tool]
