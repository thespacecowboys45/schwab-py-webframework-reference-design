from services.celery_app import celery  # Import the Celery instance from the main celery_app application
from services.redis_client import redis_client
import services.automations.automations as saa

import inspect
import time

#from logging_config import dlog

dlog_event_type_trace = {'event_type':'trace_asyncio_template'}
dlog_event_type_task = {'event_type':'task_asyncio_template'}
dlog_event_type_data = {'event_type':'data_task_asyncio_template'}

# AsyncIO Task Template (pattern is used to implement StreamClient from 'schwab-py')
FLAG_ASYNCIO_ONE_TIME_TEMPLATE_TASK_IS_RUNNING = "FLAG_ASYNCIO_ONE_TIME_TEMPLATE_TASK_IS_RUNNING"
FLAG_ASYNCIO_ONE_TIME_TEMPLATE_TASK_STATUS = "FLAG_ASYNCIO_ONE_TIME_TEMPLATE_TASK_STATUS"
FLAG_ASYNCIO_ONE_TIME_TEMPLATE_TASK_RESULT = "FLAG_ASYNCIO_ONE_TIME_TEMPLATE_TASK_RESULT"
ASYNCIO_ONE_TIME_TEMPLATE_TASK_DATA = "ASYNCIO_ONE_TIME_TEMPLATE_TASK_DATA"

task_iterations = 0

@celery.task
def task_template_asyncio_one_time():
    global task_iterations

    # For dev/debug
    fn_name = inspect.currentframe().f_code.co_name
    ex_path = f"{__name__}.{fn_name}"
    print(f"{ex_path} [ entry ]")

    redis_client.set(FLAG_ASYNCIO_ONE_TIME_TEMPLATE_TASK_IS_RUNNING, "true")
    status = {"status":"running"}
    redis_client.set(FLAG_ASYNCIO_ONE_TIME_TEMPLATE_TASK_STATUS, str(status))

    while redis_client.get(FLAG_ASYNCIO_ONE_TIME_TEMPLATE_TASK_IS_RUNNING) == b"true":
        task_iterations += 1

        print(f"{ex_path} Automations AsyncIO One-Time Task is running ... [ iterations: {task_iterations} ]")

        # Implement business logic
        do_work()

        result = {"status": "running", "iterations": task_iterations}
        redis_client.set(FLAG_ASYNCIO_ONE_TIME_TEMPLATE_TASK_RESULT, str(result))  # Store the result in Redis   

        # Simulate a long-running process
        time.sleep(5)

    status = {"status":"stopped"}
    redis_client.set(FLAG_ASYNCIO_ONE_TIME_TEMPLATE_TASK_STATUS, str(status))
    result = {"status": "stopped", "iterations": task_iterations}
    redis_client.set(FLAG_ASYNCIO_ONE_TIME_TEMPLATE_TASK_RESULT, str(result))  # Store the result in Redis        
    print(f"{ex_path} [ exit ]")

def do_work():
    # For dev/debug
    fn_name = inspect.currentframe().f_code.co_name
    ex_path = f"{__name__}.{fn_name}"
    print(f"{ex_path} [ entry ]")

    data = redis_client.get(ASYNCIO_ONE_TIME_TEMPLATE_TASK_DATA)

    if data:
        print(f"{ex_path} [ process data ]")
    else:
        print(f"{ex_path} [ no data to process ]")


def init():
    # For dev/debug
    fn_name = inspect.currentframe().f_code.co_name
    ex_path = f"{__name__}.{fn_name}"
    print(f"{ex_path} [ entry ]")

    status = {"status": "init"}
    redis_client.set(FLAG_ASYNCIO_ONE_TIME_TEMPLATE_TASK_STATUS, str(status))  # Store the result in Redis 

    result = {"result":"init"}
    redis_client.set(FLAG_ASYNCIO_ONE_TIME_TEMPLATE_TASK_RESULT, str(result))  # Store the result in Redis 

    redis_client.set(FLAG_ASYNCIO_ONE_TIME_TEMPLATE_TASK_IS_RUNNING, "false")

    print(f"{ex_path} [ task initialized ]")

