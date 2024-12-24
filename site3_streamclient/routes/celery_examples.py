from flask import Blueprint, render_template, session, jsonify, request, g
import services.celery_app
from services.redis_client import redis_client
import services.automations.automations_asyncio_task_template as asyncio_task
import services.automations.automations_poller_task_template as poller_task
import services.automations.automations_queue_task_template as queue_task
import services.automations.automations as saa
import inspect

celery_examples_bp = Blueprint('celery_examples', __name__, url_prefix='/celery_examples')

# ####################### CELERY #########################
# Celery route
@celery_examples_bp.route('/')
def home():
    # debug
    #return render_template('website_navigation/documentation.html', title="Celery Page", task_status='init')
    return render_template('celery_examples/celery_examples.html', base_template=g.base_template, title="Celery Page", task_status='init')

@celery_examples_bp.route('/celery/health', methods=['GET'])
def celery_health():
    if services.celery_app.is_celery_running():
        return {'status': 'Celery is running'}, 200
    else:
        return {'status': 'Celery is not running'}, 503

# ---------------------------------------------------------------------------------------

# Start task route
@celery_examples_bp.route('/celery_start_template_task', methods=['POST'])
def celery_start_template_task():
    # For dev/debug
    fn_name = inspect.currentframe().f_code.co_name
    ex_path = f"{__name__}.{fn_name}"
    print(f"{ex_path} [ entry ]")

    requestData = request.get_json()
    taskName = requestData.get('taskName')

    print(f"celery_start_template_task [ entry ] [ taskName: {taskName} ]")

    # First check if celery is running
    if not services.celery_app.is_celery_running():
        return jsonify({"running_status": "celery is not running yo", "task_status":"unknown", "task_result":"unknown"}), 200

    # Pythons version of a switch statement
    match taskName:
        case "asyncio_one_time":
            status = redis_client.get(asyncio_task.FLAG_ASYNCIO_ONE_TIME_TEMPLATE_TASK_STATUS)
            result = redis_client.get(asyncio_task.FLAG_ASYNCIO_ONE_TIME_TEMPLATE_TASK_RESULT)

            if redis_client.get(asyncio_task.FLAG_ASYNCIO_ONE_TIME_TEMPLATE_TASK_IS_RUNNING) == b"true":
                return jsonify({"running_status": "already running", "task_status":status.decode('utf-8') if status else "unknown", "task_result":result.decode('utf-8') if result else "unknown"}), 200
            else:
                task = asyncio_task.task_template_asyncio_one_time.apply_async()  # Start the task asynchronously

            task_set_to_run = redis_client.get(asyncio_task.FLAG_ASYNCIO_ONE_TIME_TEMPLATE_TASK_IS_RUNNING)

        case "poller":
            status = redis_client.get(poller_task.FLAG_POLLER_TEMPLATE_TASK_STATUS)
            result = redis_client.get(poller_task.FLAG_POLLER_TEMPLATE_TASK_RESULT)

            if redis_client.get(poller_task.FLAG_POLLER_TEMPLATE_TASK_IS_RUNNING) == b"true":
                return jsonify({"running_status": "already running", "task_status":status.decode('utf-8') if status else "unknown", "task_result":result.decode('utf-8') if result else "unknown"}), 200
            else:
                task = poller_task.task_template_poller.apply_async()  # Start the task asynchronously

            task_set_to_run = redis_client.get(poller_task.FLAG_POLLER_TEMPLATE_TASK_IS_RUNNING)

        case "queue":
            pass
        case _:
            print(f"Unknown task type requested to be started: {taskName}")
            return jsonify({"running_status": "unknown task " + taskName + " requested to be started", "task_status":"unknown", "task_result":"unknown"}), 200            

    if task_set_to_run:
        running_status = task_set_to_run.decode('utf-8')
        task_status = status.decode('utf-8') if status else "unknown"
        task_result = result.decode('utf-8') if result else "unknown"
    else:
        running_status = "no status"
        task_status = "unknown"
        task_result = "unknown"

    response = {
        "running_status": running_status,
        "task_status": task_status,
        "task_result": task_result
    }

    return jsonify(response), 200


# Stop task route
@celery_examples_bp.route('/celery_stop_template_task', methods=['POST'])
def celery_stop_template_task():
    # For dev/debug
    fn_name = inspect.currentframe().f_code.co_name
    ex_path = f"{__name__}.{fn_name}"
    print(f"{ex_path} [ entry ]")

    requestData = request.get_json()
    taskName = requestData.get('taskName')

    print(f"celery_stop_template_task [ entry ] [ taskName: {taskName} ]")

    # First check if celery is running
    if not services.celery_app.is_celery_running():
        return jsonify({"running_status": "celery is not running yo", "task_status":"unknown", "task_result":"unknown"}), 200

    # Pythons version of a switch statement
    match taskName:
        case "asyncio_one_time":
            redis_client.set(asyncio_task.FLAG_ASYNCIO_ONE_TIME_TEMPLATE_TASK_IS_RUNNING, "false")

            task_set_to_run = redis_client.get(asyncio_task.FLAG_ASYNCIO_ONE_TIME_TEMPLATE_TASK_IS_RUNNING)
            status = redis_client.get(asyncio_task.FLAG_ASYNCIO_ONE_TIME_TEMPLATE_TASK_STATUS)
            result = redis_client.get(asyncio_task.FLAG_ASYNCIO_ONE_TIME_TEMPLATE_TASK_RESULT)

        case "poller":
            redis_client.set(poller_task.FLAG_POLLER_TEMPLATE_TASK_IS_RUNNING, "false")

            task_set_to_run = redis_client.get(poller_task.FLAG_POLLER_TEMPLATE_TASK_IS_RUNNING)
            status = redis_client.get(poller_task.FLAG_POLLER_TEMPLATE_TASK_STATUS)
            result = redis_client.get(poller_task.FLAG_POLLER_TEMPLATE_TASK_RESULT)

        case "queue":
            pass
        case _:
            print(f"Unknown task type requested to be started: {taskName}")
            return jsonify({"running_status": "unknown task " + taskName + " requested to be stopped", "task_status":"unknown", "task_result":"unknown"}), 200            

    if task_set_to_run:
        running_status = task_set_to_run.decode('utf-8')
        task_status = status.decode('utf-8') if status else "unknown"
        task_result = result.decode('utf-8') if result else "unknown"
    else:
        running_status = "no status"
        task_status = "unknown"
        task_result = "unknown"

    response = {
        "running_status": running_status,
        "task_status": task_status,
        "task_result": task_result
    }

    return jsonify(response), 200


@celery_examples_bp.route('/celery_get_template_task_status', methods=['POST'])
def celery_get_template_task_status():
    # For dev/debug
    fn_name = inspect.currentframe().f_code.co_name
    ex_path = f"{__name__}.{fn_name}"
    print(f"{ex_path} [ entry ]")

    requestData = request.get_json()
    taskName = requestData.get('taskName')

    print(f"{ex_path} celery_stop_template_task [ entry ] [ taskName: {taskName} ]")

    # First check if celery is running
    if not services.celery_app.is_celery_running():
        return jsonify({"running_status": "celery is not running yo", "task_status":"", "task_result":""}), 200

    # Pythons version of a switch statement
    match taskName:
        case "asyncio_one_time":
            task_set_to_run = redis_client.get(asyncio_task.FLAG_ASYNCIO_ONE_TIME_TEMPLATE_TASK_IS_RUNNING)
            status = redis_client.get(asyncio_task.FLAG_ASYNCIO_ONE_TIME_TEMPLATE_TASK_STATUS)
            result = redis_client.get(asyncio_task.FLAG_ASYNCIO_ONE_TIME_TEMPLATE_TASK_RESULT)


        case "poller":
            task_set_to_run = redis_client.get(poller_task.FLAG_POLLER_TEMPLATE_TASK_IS_RUNNING)
            status = redis_client.get(poller_task.FLAG_POLLER_TEMPLATE_TASK_STATUS)
            result = redis_client.get(poller_task.FLAG_POLLER_TEMPLATE_TASK_RESULT)

        case "queue":
            pass
        case _:
            return jsonify({"running_status": "unknown task " + taskName + " requested for status", "task_status":"", "task_result":""}), 200            

    if task_set_to_run:
        running_status = task_set_to_run.decode('utf-8')
        task_status = status.decode('utf-8') if status else "unknown"
        task_result = result.decode('utf-8') if result else "unknown"
    else:
        running_status = "no status"
        task_status = "unknown"
        task_result = "unknown"

    response = {
        "running_status": running_status,
        "task_status": task_status,
        "task_result": task_result
    }

    return jsonify(response), 200
