import functools
import multiprocessing.pool
import string
import random


def timeout(timeout):
    """Decorator that limits functions execution time.

    :Raises TimeoutError: when function execution time exceeds timeout.
    """

    def timeout_decorator(item):

        @functools.wraps(item)
        def func_wrapper(*args, **kwargs):
            pool = multiprocessing.pool.ThreadPool(processes=1)
            async_result = pool.apply_async(item, args, kwargs)
            return async_result.get(timeout)

        return func_wrapper

    return timeout_decorator


def get_random_str(size=14):
    chars = string.ascii_lowercase + string.digits
    return ''.join(random.choice(chars) for _ in range(size))
