from collections.abc import Callable
from functools import wraps
from time import time
from typing import ParamSpec, TypeVar

from loguru import logger


F_Spec = ParamSpec("F_Spec")
F_Return = TypeVar("F_Return")


def time_it(total: int) -> Callable[[Callable[F_Spec, F_Return]], Callable[F_Spec, F_Return]]:
    def inner_decorator(func: Callable[F_Spec, F_Return]) -> Callable[F_Spec, F_Return]:
        @wraps(func)
        def wrapper(*args: F_Spec.args, **kwargs: F_Spec.kwargs) -> F_Return:
            start_time = time()
            result = func(*args, **kwargs)
            end_time = time()
            delta_time = end_time - start_time
            speed_time = delta_time / total
            logger.info(f"Скорость обработки {total} записей: {delta_time} секунд")
            logger.info(f"Средняя скорость обработки одной записи из {total} записей: {speed_time} секунд")
            return result

        return wrapper

    return inner_decorator
