import asyncio
from fastmcp import Client

client = Client("servers/basic-stdio-server.py") 

async def calltool(city: str):
    async with client:
        result = await client.call_tool("get_temprature", {"city": city})
        print(result)


asyncio.run(calltool("mumbai"))
