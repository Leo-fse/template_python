from config.log_config import log_decorator


@log_decorator
def inner_module_example():
    print("inner_module_example")
