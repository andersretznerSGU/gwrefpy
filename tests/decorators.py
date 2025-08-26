def timed(iters=1):
    """Decorator to time a function."""
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
                print(
                    f"Function {func.__name__} took {(end_time - start_time) / iters:.4f} seconds on average over {iters} iterations."
                )
            else:
                print(
                    f"Function {func.__name__} took {end_time - start_time:.4f} seconds."
                )
            return result

        return wrapper

    return decorator


def print_return(func):
    """Decorator to print the return value of a function."""

    def wrapper(*args, **kwargs):
        """Wrapper function that prints the return value."""
        result = func(*args, **kwargs)
        print(f"Return value of {func.__name__}: {result}")
        return result

    return wrapper
