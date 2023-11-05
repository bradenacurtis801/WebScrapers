import time
import warnings
import functools
from colorama import init, Fore

# Initialize Colorama
init()

def timing_decorator(func):
    """
    A decorator that prints the time a function takes to execute in different colors.
    """
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        start_time = time.perf_counter()  # Start the timer
        result = func(*args, **kwargs)  # Call the original function
        end_time = time.perf_counter()  # End the timer
        execution_time = end_time - start_time

        # Define time thresholds for different colors
        thresholds = {
            'red': 5,     # Red for more than 5 seconds
            'yellow': 1,  # Yellow for more than 1 second and less than or equal to 5 seconds
            'green': 0    # Green for 1 second or less
        }

        # Choose the color
        if execution_time > thresholds['red']:
            color = Fore.RED
        elif execution_time > thresholds['yellow']:
            color = Fore.YELLOW
        else:
            color = Fore.GREEN

        # Print the formatted message with the selected color
        print(color + f"{func.__name__} executed in {execution_time:.2f} seconds" + Fore.RESET)
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

def decorator_record_algorithm_type(func):
    """
    A decorator that records the algorithm or function type used.
    """
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        # Perform the recording here, e.g., by printing or logging
        label = f"Algorithm/Function used: {func.__name__}\n\n"
        print(label)
        # Call the original function
        result = label + func(*args, **kwargs)
        return result
    return wrapper