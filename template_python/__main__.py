import subprocess

from config.log_config import log_decorator, logger
from template_python.libs.database import OracleDatabase
from template_python.libs.inner_module_example import inner_module_example
from template_python.setting import OUTER_MODULE_DIR, config, debug


@log_decorator
def execute_outer_module(execute_task_list: list[str] = ["outer_module_example.py"]):
    for task in execute_task_list:
        module_example_path = OUTER_MODULE_DIR / task
        logger.info(f"{task} is running")
        try:
            if debug:
                # デバッグ時の設定
                subprocess.run(["python", "-Xfrozen_modules=off", module_example_path], check=True)
            else:
                # 本番環境の設定
                subprocess.run(["python", module_example_path], check=True)
        except subprocess.CalledProcessError as e:
            logger.error(f"Error occurred while running {task}: {e}", exc_info=True)
        else:
            logger.info(f"{task} is finished")


@log_decorator
def main():
    inner_module_example()
    logger.debug("main is finished")
    logger.info("main is finished")
    logger.warning("main is finished")
    logger.error("main is finished")
    logger.critical("main is finished")
    # db_config = config["Development"]
    # o = OracleDatabase(db_config)
    # data = o.fetch_data("select * from test")
    # print(data)


if __name__ == "__main__":
    main()
