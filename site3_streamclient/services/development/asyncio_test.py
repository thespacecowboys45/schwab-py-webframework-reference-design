import asyncio

# Variable to store the background task
background_task = None

# To integrate threading and asyncio
background_task_thread = None

# A value to return to the client
latest_value = 0

# Define the background async function
async def run_background_task():
    global latest_value
    print(f"module_asyncio_test.py [ run_background_task() ] [ entry ]")

    while True:
        print(f"module_asyncio_test.py [ Background task is running...] [ latest_value: {latest_value} ]")
        latest_value += 1

        await asyncio.sleep(3)  # Example task with sleep


#
#  DESIGN GOAL: 
# This module will have a background task updating a variable
# It will also have streaming capabilities to return the latest value to the client (browser)
# We can start / stop the task thread
# We can start / stop the streaming
#