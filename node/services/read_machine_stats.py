import random


async def generate_fake_status():
    return {
        "temperature": random.randint(0, 100),
        "humidity": random.randint(0, 100),
        "pressure": random.randint(0, 100),
        "power": random.randint(0, 100),
    }


async def read_machine_status():
    machine_status = await generate_fake_status()
    return machine_status
