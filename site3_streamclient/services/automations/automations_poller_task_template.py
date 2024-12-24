from services.celery_app import celery  # Import the Celery instance from the main celery_app application
from services.redis_client import redis_client

import inspect
import time

# Poller Task Template
FLAG_POLLER_TEMPLATE_TASK_IS_RUNNING = "FLAG_POLLER_TEMPLATE_TASK_IS_RUNNING"
FLAG_POLLER_TEMPLATE_TASK_STATUS = "FLAG_POLLER_TEMPLATE_TASK_STATUS"
FLAG_POLLER_TEMPLATE_TASK_RESULT = "FLAG_POLLER_TEMPLATE_TASK_RESULT"
POLLER_TEMPLATE_TASK_DATA = "POLLER_TEMPLATE_TASK_DATA"

task_iterations = 0

@celery.task
def task_template_poller():
    global task_iterations

    # For dev/debug
    fn_name = inspect.currentframe().f_code.co_name
    ex_path = f"{__name__}.{fn_name}"
    print(f"{ex_path} [ entry ]")

    redis_client.set(FLAG_POLLER_TEMPLATE_TASK_IS_RUNNING, "true")
    status = {"status":"running"}
    redis_client.set(FLAG_POLLER_TEMPLATE_TASK_STATUS, str(status))

    while redis_client.get(FLAG_POLLER_TEMPLATE_TASK_IS_RUNNING) == b"true":
        task_iterations += 1

        print(f"{ex_path} Automations QuoteCollector Task is running ... [ iterations: {task_iterations} ]")

        # Implement business logic
        do_work()

        result = {"status": "running", "iterations": task_iterations}
        redis_client.set(FLAG_POLLER_TEMPLATE_TASK_RESULT, str(result))  # Store the result in Redis   

        # Simulate a long-running process
        time.sleep(5)

    status = {"status":"stopped"}
    redis_client.set(FLAG_POLLER_TEMPLATE_TASK_STATUS, str(status))
    result = {"status": "stopped", "iterations": task_iterations}
    redis_client.set(FLAG_POLLER_TEMPLATE_TASK_RESULT, str(result))  # Store the result in Redis        
    print(f"{ex_path} [ exit ]")

def do_work():
    # For dev/debug
    fn_name = inspect.currentframe().f_code.co_name
    ex_path = f"{__name__}.{fn_name}"
    print(f"{ex_path} [ entry ]")

    data = redis_client.get(POLLER_TEMPLATE_TASK_DATA)

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
    redis_client.set(FLAG_POLLER_TEMPLATE_TASK_STATUS, str(status))  # Store the result in Redis 

    result = {"result":"init"}
    redis_client.set(FLAG_POLLER_TEMPLATE_TASK_RESULT, str(result))  # Store the result in Redis 

    redis_client.set(FLAG_POLLER_TEMPLATE_TASK_IS_RUNNING, "false")

    print(f"{ex_path} [ task initialized ]")

