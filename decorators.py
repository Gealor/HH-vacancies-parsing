from functools import wraps
import json
import logging
import time
from typing import Callable
import orjson

log = logging.getLogger(__name__)


def time_meter_decorator(func: Callable):
    @wraps(func)
    async def wrapper(*args, **kwargs): # для асинхронного декоратора пишем функцию обертку через await, т.к. в ней вызывается основая асинхронная функция, а внешняя функция возвращает лишь объект функции, не ее результат
        start = time.time()
        result = await func(*args, **kwargs)
        end = time.time() - start
        print(f"Function {func.__name__} | {end} seconds")
        return result
    return wrapper


def write_into_file(filepath: str):
    def inner_func(func: Callable):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            result = await func(*args, **kwargs)
            try:
                with open(filepath, mode='w', encoding='utf-8') as file:
                    file.write(orjson.dumps(result).decode(encoding='utf-8'))
            except Exception as e:
                log.error("Failed to write data into file: %s", e)
            else:
                log.info("Vacancies write into file: %d", len(result))
            return result
        return wrapper
    return inner_func

