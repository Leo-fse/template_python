import functools
import logging
import time
import traceback

from template_python.setting import LOG_DIR

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
myhandler = logging.StreamHandler()
myhandler.setFormatter(logging.Formatter("%(asctime)s - %(levelname)s - %(message)s"))
logger.addHandler(myhandler)

# ログ出力は実行日時毎に分ける
file_handler = logging.FileHandler(LOG_DIR / f"log_{time.strftime('%Y%m%d_%H%M%S')}.log")
file_handler.setFormatter(logging.Formatter("%(asctime)s - %(levelname)s - %(message)s"))
logger.addHandler(file_handler)


def log_decorator(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        try:
            logger.info(f"START   {func.__module__}.{func.__name__} args: {args}, kwargs: {kwargs}")
            start_time = time.time()
            result = func(*args, **kwargs)
            end_time = time.time()
            logger.info(f"FINISHED {func.__name__} executed_time: {end_time - start_time:.2f} seconds")
            return result
        except Exception as e:
            logger.error(f"ERROR in {func.__name__} : {traceback.format_exc()}")
            raise

    return wrapper
