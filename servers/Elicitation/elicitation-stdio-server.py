from fastmcp import FastMCP, Context
from dataclasses import dataclass

mcp = FastMCP("Elicition server")

@dataclass
class UserInfo:
    name: str
    age: int

@mcp.tool
async def collect_user_info(ctx: Context) -> str:
    """Collect user information through interactive prompts."""

    result = await ctx.elicit(
        message="please provide your information",
        response_type=UserInfo
    )

    if result.action == "accept":
        user = result.data
        return f"Hello {user.name}, you are {user.age} years old"
    elif result.action == "decline":
        return "Information not provided"
    else:  # cancel
        return "Operation cancelled"

@mcp.tool
async def plan_meeting(ctx: Context) -> str:
    """Plan a meeting by gathering details step by step."""

    title_result = await ctx.elicit("What's the meeting title?", response_type=str)
    if title_result.action != "accept":
        return "Meeting planning cancelled"

    duration_result = await ctx.elicit("Duration in minutes?", response_type=int)
    if duration_result.action != "accept":
        return "Meeting planning cancelled"

    meeting_cat_result = await ctx.elicit(
        "Choose Meeting category",
        response_type=[["technical", "functional", "UAT"]]  # Note: list of a list
    )
    if meeting_cat_result.action != "accept":
            return "Meeting planning cancelled"

    priority_result = await ctx.elicit(
        "Is this urgent?",
        response_type=["yes", "no"]
    )
    if priority_result.action != "accept":
        return "Meeting planning cancelled"

    urgent = priority_result.data == "yes"
    return f"Meeting '{title_result.data}' for {duration_result.data} minutes with category {meeting_cat_result.data} (Urgent: {urgent})"

@mcp.tool
async def approve_action(ctx: Context) -> str:
    result = await ctx.elicit("Approve this action?", response_type=bool)

    if result.action == "accept" and result.data:
        return "Action accepted"
    else:
        raise ValueError("Action rejected")

if __name__ == "__main__":
    mcp.run()