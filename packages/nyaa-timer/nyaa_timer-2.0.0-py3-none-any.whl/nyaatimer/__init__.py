from time import perf_counter
from rich import print as rprint


def nyaatimer(func):
    def wrapper(*args, **kwargs):
        start_time = perf_counter()
        result = func(*args, **kwargs)
        end_time = perf_counter()
        rprint(f"Function {func.__name__} took {end_time - start_time} seconds")
        rprint(f"Args={args}, Kwargs={kwargs}")
        return result

    return wrapper
