## imports
import logging
from fastmcp import FastMCP, Context

## Create MCP server
mcp = FastMCP("Sampling Demo")

logger = logging.getLogger("sampling-demo-mcp")


@mcp.tool
async def summarize_text(text: str, ctx: Context) -> str:
    """Ask the caller's LLM to summarize the provided text in 2 sentences."""

    logger.info("Requesting summary via client sampling")

    response = await ctx.sample(
        messages=[f"Summarize the following text in exactly two sentences:\n\n{text}"],
        system_prompt="You are a concise summarization assistant.",
        max_tokens=256,
        temperature=0.3,
    )

    # response.text works for TextContent replies from the client's LLM
    return getattr(response, "text", str(response))


@mcp.tool
async def brainstorm_ideas(topic: str, count: int, ctx: Context) -> list[str]:
    """Ask the caller's LLM to brainstorm `count` short ideas about a topic."""

    if count <= 0:
        return []

    logger.info(f"Brainstorming {count} ideas about {topic}")

    response = await ctx.sample(
        messages=[
            f"Give me {count} short, distinct ideas about: {topic}. "
            "Return one idea per line, no numbering, no extra commentary."
        ],
        system_prompt="You are a creative brainstorming partner.",
        max_tokens=400,
        temperature=0.8,
    )

    raw = getattr(response, "text", str(response))
    ideas = [line.strip("-* \t") for line in raw.splitlines() if line.strip()]
    return ideas[:count]


if __name__ == "__main__":
    logger.info("Sampling demo MCP server starting")
    mcp.run("http", host="0.0.0.0", port=8004)
