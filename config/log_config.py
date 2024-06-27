import functools
import logging
import os
import re
import time
import traceback

from colorama import Fore, Style, init

from template_python.setting import LOG_DIR

init(autoreset=True)


class ColoredFormatter(logging.Formatter):
    def format(self, record):
        log_colors = {
            "DEBUG": Fore.CYAN,
            "INFO": Fore.GREEN,
            "WARNING": Fore.YELLOW,
            "ERROR": Fore.RED,
            "CRITICAL": Fore.RED,
        }
        log_color = log_colors.get(record.levelname, Fore.RESET)
        record.levelname = f"{log_color}{record.levelname}{Style.RESET_ALL}"
        return super().format(record)


logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
console_handler = logging.StreamHandler()
console_handler.setFormatter(ColoredFormatter("%(asctime)s - %(levelname)s - %(message)s"))
logger.addHandler(console_handler)

# ログ出力は実行日時毎に分ける

# ログファイルのパス
log_file_path = LOG_DIR / f"log_{time.strftime('%Y%m%d_%H%M%S')}.log"

# ログファイルの履歴を10回分残して、それ以上は削除するように修正
log_dir = LOG_DIR
log_file_pattern = "log_*.log"
log_files = sorted(log_dir.glob(log_file_pattern), key=os.path.getctime, reverse=True)

# ログファイルの履歴を10回分残して、それ以上は削除
if len(log_files) > 10:
    for file_to_delete in log_files[10:]:
        os.remove(file_to_delete)

file_handler = logging.FileHandler(log_file_path)
file_handler.setFormatter(
    logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
)  # カラーコードを削除
logger.addHandler(file_handler)


def log_decorator(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        try:
            logger.info(f"START   {func.__module__}.{func.__name__} args: {args}, kwargs: {kwargs}")
            start_time = time.time()
            result = func(*args, **kwargs)
            end_time = time.time()
            logger.info(
                f"FINISHED {func.__name__} executed_time: {end_time - start_time:.2f} seconds"
            )
            return result
        except Exception:
            logger.error(f"ERROR in {func.__name__} : {traceback.format_exc()}")
            raise
        finally:
            # カラーコードを削除
            remove_color_codes(log_file_path)

    return wrapper


def remove_color_codes(log_file_path):
    with open(log_file_path, "r") as file:
        log_content = file.read()

    # カラーコードを削除する正規表現パターン
    color_code_pattern = re.compile(r"\x1b\[\d+m")

    # カラーコードを削除
    log_content = re.sub(color_code_pattern, "", log_content)

    with open(log_file_path, "w") as file:
        file.write(log_content)
