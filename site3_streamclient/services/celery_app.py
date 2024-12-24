from celery import Celery
import inspect


def make_celery():
    fn_name = inspect.currentframe().f_code.co_name
    ex_path = f"{__name__}.{fn_name}"
    print(f"{ex_path} [ entry ]")  

    #celery = Celery(app.import_name, broker=app.config['CELERY_BROKER_URL'])
    celery = Celery('my_app')

    # Configure broker and backend
    celery.conf.broker_url = 'redis://localhost:6379/0'
    celery.conf.result_backend = 'redis://localhost:6379/0'

    #celery.conf.update(app.config)
    
    celery.Task = type('ContextTask', (celery.Task,), {'__call__': lambda s, *a, **k: s.run(*a, **k)})
    return celery

celery = make_celery()

def is_celery_running():
    fn_name = inspect.currentframe().f_code.co_name
    ex_path = f"{__name__}.{fn_name}"
    print(f"{ex_path} [ entry ]")  

    try:
        # Send a ping and wait for a response
        result = celery.control.ping(timeout=1)
        return bool(result)  # Returns True if at least one worker responds
    except Exception:
        return False