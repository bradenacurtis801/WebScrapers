import time
import warnings
import functools
from colorama import init, Fore

# Initialize Colorama
init()

def timing_decorator(func):
    """
    A decorator that prints the time a function takes to execute.
    """
    def wrapper(*args, **kwargs):
        start_time = time.perf_counter()  # Start the timer
        result = func(*args, **kwargs)  # Call the original function
        end_time = time.perf_counter()  # End the timer
        print(f"{func.__name__} executed in {end_time - start_time:.2f} seconds")
        return result
    return wrapper

def deprecated(func):
    """This is a decorator which can be used to mark functions as deprecated."""
    @functools.wraps(func)
    def new_func(*args, **kwargs):
        warnings.warn(Fore.YELLOW + f"Call to deprecated function {func.__name__}." + Fore.RESET,
                      category=DeprecationWarning, stacklevel=2)
        return func(*args, **kwargs)
    return new_func