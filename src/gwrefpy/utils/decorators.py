import logging

logger = logging.getLogger(__name__)


def timed(iters=1):
    """Decorator to time a function.
    Parameters
    ----------
    iters : int
        Number of iterations to run the function for timing. Default is 1.

    Returns
    -------
    decorator : function
        The decorator function."""
    import time

    def decorator(func):
        """Decorator function that wraps the original function."""

        def wrapper(*args, **kwargs):
            """Wrapper function to time the execution of the decorated function."""
            if iters <= 0:
                raise ValueError("Number of iterations must be a positive integer.")

            result = None
            start_time = time.time()
            for _ in range(iters):
                result = func(*args, **kwargs)
            end_time = time.time()
            if iters > 1:
                logger.info(
                    f"Function {func.__name__} took"
                    f" {(end_time - start_time) / iters:.4f}"
                    f" seconds on average over {iters} iterations."
                )
            else:
                logger.info(
                    f"Function {func.__name__} took"
                    f" {end_time - start_time:.4f} seconds."
                )
            return result

        return wrapper

    return decorator


def print_return(func):
    """Decorator to print the return value of a function.
    Parameters
    ----------
    func : function
        The function whose return value is to be printed.

    Returns
    -------
    None
        The return value of the decorated function is printed to the console."""

    def wrapper(*args, **kwargs):
        """Wrapper function that prints the return value."""
        result = func(*args, **kwargs)
        logger.info(f"Return value of {func.__name__}: {result}")
        return result

    return wrapper
