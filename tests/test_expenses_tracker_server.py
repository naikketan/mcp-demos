import json

import pytest
from fastmcp import Client


async def test_add_expense_returns_success_message(expenses_server):
    async with Client(expenses_server.mcp) as client:
        result = await client.call_tool(
            "add_expense",
            {
                "date": "2026-01-15",
                "amount": 42.50,
                "category": "food",
                "description": "Lunch with team",
                "payment_method": "visa",
            },
        )

    assert "Successfully added expense" in result.content[0].text
    assert "42.5" in result.content[0].text


async def test_add_expense_persists_to_memory(expenses_server):
    async with Client(expenses_server.mcp) as client:
        await client.call_tool(
            "add_expense",
            {
                "date": "2026-02-01",
                "amount": 100.0,
                "category": "gadget",
                "description": "USB-C hub",
                "payment_method": "amex",
            },
        )

    assert len(expenses_server.EXPENSES) == 1
    assert expenses_server.EXPENSES[0] == {
        "date": "2026-02-01",
        "amount": 100.0,
        "category": "gadget",
        "description": "USB-C hub",
        "payment_method": "amex",
    }


async def test_add_expense_rejects_non_positive_amount(expenses_server):
    async with Client(expenses_server.mcp) as client:
        result = await client.call_tool(
            "add_expense",
            {
                "date": "2026-03-10",
                "amount": 0,
                "category": "other",
                "description": "invalid",
                "payment_method": "cash",
            },
        )

    assert "Error" in result.content[0].text
    assert expenses_server.EXPENSES == []


async def test_add_expense_rejects_invalid_category(expenses_server):
    async with Client(expenses_server.mcp) as client:
        with pytest.raises(Exception):
            await client.call_tool(
                "add_expense",
                {
                    "date": "2026-03-10",
                    "amount": 10.0,
                    "category": "not-a-real-category",
                    "description": "bad",
                    "payment_method": "cash",
                },
            )


async def test_expenses_resource_returns_all_expenses(expenses_server):
    async with Client(expenses_server.mcp) as client:
        await client.call_tool(
            "add_expense",
            {
                "date": "2026-04-01",
                "amount": 15.0,
                "category": "transport",
                "description": "Bus fare",
                "payment_method": "cash",
            },
        )

        result = await client.read_resource("resource://expenses-memory")

    payload = json.loads(result[0].text)
    assert len(payload) == 1
    assert payload[0]["description"] == "Bus fare"


async def test_analyze_spending_prompt_includes_filters(expenses_server):
    async with Client(expenses_server.mcp) as client:
        result = await client.get_prompt(
            "analyze_spending_prompt",
            {"category": "food", "start_date": "2026-01-01", "end_date": "2026-01-31"},
        )

    text = result.messages[0].content.text
    assert "Category: food" in text
    assert "From: 2026-01-01" in text
    assert "To: 2026-01-31" in text


async def test_analyze_spending_prompt_without_filters(expenses_server):
    async with Client(expenses_server.mcp) as client:
        result = await client.get_prompt("analyze_spending_prompt", {})

    text = result.messages[0].content.text
    assert "Please analyze my spending patterns" in text
    assert "Category:" not in text


async def test_server_exposes_expected_tools(expenses_server):
    async with Client(expenses_server.mcp) as client:
        tools = await client.list_tools()

    assert [t.name for t in tools] == ["add_expense"]
