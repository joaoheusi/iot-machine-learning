import asyncio

from providers.ml_server import post_data
from services.read_machine_stats import read_machine_status


async def main():
    while True:
        machine_status = await read_machine_status()
        response = await post_data(machine_status)
        print(response)
        print("\n")
        import time

        time.sleep(3)


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
