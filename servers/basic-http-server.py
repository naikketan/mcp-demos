from fastmcp import FastMCP

mcp = FastMCP("My Http Demo server")

@mcp.tool
def add_number(a: int, b: int) -> int:
    """Add Two number."""
    return a + b

if __name__ == "__main__":
    mcp.run(transport="http", host="127.0.0.1", port=8000)