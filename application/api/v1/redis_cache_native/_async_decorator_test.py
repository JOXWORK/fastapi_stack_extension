from functools import wraps


def my_decorator(func):
    @wraps(func)
    async def wrapper(*args, **kwargs):
        print("Some do before", args, kwargs)
        result = await func(*args, **kwargs)
        print("Some do after")

        return result

    return wrapper


def callable_decorator(A=None, B=None):
    def decorator(func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            print("Arg A", A)
            result = await func(*args, **kwargs)
            print("Arg B", B)

            return result

        return wrapper

    return decorator
