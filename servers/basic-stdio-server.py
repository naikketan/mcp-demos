from fastmcp import FastMCP

mcp = FastMCP("My Demo Server")

@mcp.tool
def get_temprature(city: str) -> str:
    """Get current whether of city"""
    return f"Temprature in {city} is 20 celcius"

if __name__ == "__main__":
    mcp.run()
