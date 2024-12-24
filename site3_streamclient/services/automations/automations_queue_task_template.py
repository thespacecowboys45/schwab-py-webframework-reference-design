from services.celery_app import celery  # Import the Celery instance from the main celery_app application
from services.redis_client import redis_client
import services.automations.automations as saa

import inspect
import time

#from logging_config import dlog

dlog_event_type_trace = {'event_type':'trace_queue_template'}
dlog_event_type_task = {'event_type':'task_queue_template'}
dlog_event_type_data = {'event_type':'data_task_queue_template'}

task_iterations = 0

@celery.task
def task_queue_template():
    global task_iterations

    # For dev/debug
    fn_name = inspect.currentframe().f_code.co_name
    ex_path = f"{__name__}.{fn_name}"
    print(f"{ex_path} [ entry ]")

    redis_client.set(saa.FLAG_QUEUE_TEMPLATE_TASK_IS_RUNNING, "true")

    while redis_client.get(saa.FLAG_QUEUE_TEMPLATE_TASK_IS_RUNNING) == b"true":
        task_iterations += 1

        print(f"{ex_path} Automations QuoteCollector Task is running ... [ iterations: {task_iterations} ]")

        # Implement business logic
        timeout = 5
        do_work(timeout)

        result = {"status": "running", "iterations": task_iterations}
        redis_client.set(saa.FLAG_QUEUE_TEMPLATE_TASK_STATUS, str(result))  # Store the result in Redis   

        # Simulate a long-running process
        time.sleep(5)

    result = {"status": "stopped", "iterations": task_iterations}
    redis_client.set(saa.FLAG_QUEUE_TEMPLATE_TASK_STATUS, str(result))  # Store the result in Redis        
    print(f"{ex_path} [ exit ]")

def do_work(timeout):
    # For dev/debug
    fn_name = inspect.currentframe().f_code.co_name
    ex_path = f"{__name__}.{fn_name}"
    print(f"{ex_path} [ entry ]")

    data = redis_client.blpop(saa.QUEUE_QUEUE_TEMPLATE_DATA, timeout=timeout)

    if data:
        print(f"{ex_path} [ process data ]")
    else:
        print(f"{ex_path} [ no data to process ]")


# @param data - json
def enqueueData(data=None):
    # For dev/debug
    fn_name = inspect.currentframe().f_code.co_name
    ex_path = f"{__name__}.{fn_name}"
    print(f"{ex_path} [ entry ]")
    dlog.info(f"{ex_path} [ entry ]", extra=dlog_event_type_trace)  

    if data is None:
        print(f"{ex_path} NO DATA TO enqueue")
        dlog.error(f"{ex_path} NO DATA TO enqueue", extra=dlog_event_type_task)
        return None

    #print(f"{ex_path} attempt to enqueue: {data}")        
    print(f"{ex_path} attempt to enqueue data")       
    dlog.info(f"{ex_path} attempt to enqueue data", extra=dlog_event_type_task)        

    try:
        # Serialize the object to a JSON string
        data_str = json.dumps(data)
        redis_client.rpush(saa.QUEUE_QUEUE_TEMPLATE_DATA, data_str)
    except Exception as e:
        print(f"{ex_path} Error enqueueing data: {e}")

    print(f"{ex_path} [ exit ]")
    dlog.info(f"{ex_path} [ exit ]", extra=dlog_event_type_trace)

def init():
    # For dev/debug
    fn_name = inspect.currentframe().f_code.co_name
    ex_path = f"{__name__}.{fn_name}"
    print(f"{ex_path} [ entry ]")

    status = {"status": "init"}
    redis_client.set(saa.FLAG_QUEUE_TEMPLATE_TASK_STATUS, str(status))  # Store the result in Redis 

    if redis_client.get(saa.FLAG_QUEUE_TEMPLATE_TASK_IS_RUNNING) == b"true":
        redis_client.set(saa.FLAG_QUEUE_TEMPLATE_TASK_IS_RUNNING, "false")


    print(f"{ex_path} [ task initialized ]")
