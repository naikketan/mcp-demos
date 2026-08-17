import logging
from enum import Enum
from typing import Annotated
from datetime import date

from fastmcp import FastMCP

## Create MCP server
mcp = FastMCP("Expenses Tracker In-Memory HTTP")

# Initialize logging
logger = logging.getLogger("Expenses tracker in-memory mcp")

# In-memory storage
EXPENSES: list[dict[str, object]] = []


class PaymentMethod(Enum):
    AMEX = "amex"
    VISA = "visa"
    CASH = "cash"


class Category(Enum):
    FOOD = "food"
    TRANSPORT = "transport"
    ENTERTAINMENT = "entertainment"
    SHOPPING = "shopping"
    GADGET = "gadget"
    OTHER = "other"


@mcp.tool
async def add_expense(
    date: Annotated[date, "Date of expenses in YYYY-MM-DD format"],
    amount: Annotated[float, "Positive numeric amount of the expense"],
    category: Annotated[Category, "Category label"],
    description: Annotated[str, "Human-readable description of the expense"],
    payment_method: Annotated[PaymentMethod, "Payment method used"],
):
    """Add a new expense to the in-memory list."""

    if amount <= 0:
        return "Error: amount must be positive number"

    date_iso = date.isoformat()
    expense = {
        "date": date_iso,
        "amount": amount,
        "category": category.value,
        "description": description,
        "payment_method": payment_method.value,
    }

    EXPENSES.append(expense)
    logger.info(f"Added expense: ${amount} for {description} on {date_iso}")
    return f"Successfully added expense: ${amount} for {description} on {date_iso}"


@mcp.resource("resource://expenses-memory")
async def get_expenses_data():
    """Return the full in-memory list of expenses."""
    logger.info("Expenses data accessed from memory")
    return EXPENSES


@mcp.prompt
def analyze_spending_prompt(
    category: str | None = None, start_date: str | None = None, end_date: str | None = None
) -> str:
    """Generate a prompt to analyze spending patterns with optional filters."""

    filters = []
    if category:
        filters.append(f"Category: {category}")
    if start_date:
        filters.append(f"From: {start_date}")
    if end_date:
        filters.append(f"To: {end_date}")

    filter_text = f" ({', '.join(filters)})" if filters else ""

    return f"""
    Please analyze my spending patterns{filter_text} and provide:

    1. Total spending breakdown by category
    2. Average daily/weekly spending
    3. Most expensive single transaction
    4. Payment method distribution
    5. Spending trends or unusual patterns
    6. Recommendations for budget optimization

    Use the expense data to generate actionable insights.
    """


if __name__ == "__main__":
    logger.info("MCP Expenses server starting (HTTP mode on port 8002)")
    mcp.run("http", host="0.0.0.0", port=8003)
