import asyncio


async def weather_background_service(is_canceled: bool):
    while is_canceled is not True:
        print("Background service is running...")
        await asyncio.sleep(5)


# Define a main function that does some work in parallel with the background service
async def main_work():
    for i in range(10):
        print(f"Main work iteration {i}")
        await asyncio.sleep(1)  # Simulate some work with a delay


# Set up the event loop
async def main():
    is_canceled: bool = False;
    # Run the background service as a separate asyncio task
    background_task = asyncio.create_task(weather_background_service(is_canceled));

    # Run other main work concurrently
    await main_work()

    # Optionally, wait for the background task to finish if needed (here it runs indefinitely)
    # await background_task

# Start the asyncio event loop
asyncio.run(main())
