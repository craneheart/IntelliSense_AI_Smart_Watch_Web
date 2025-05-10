import asyncio

from ws_class import UnitAdmin


async def main():
    unit = UnitAdmin()
    await unit.connection()


asyncio.run(main())
