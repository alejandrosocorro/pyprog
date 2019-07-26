from functools import lru_cache as cache


@cache(maxsize=None)
def fib(n: int) -> int:
    """
    Cache the results of previous fib calls so that
    so when you need them again, you can look them up
    instead of needing to compute again for the nth time.

    The maxsize property indicates how many of the most recent calls
    of the function it is decorating should be cached.
    Setting it to None indicates that there is no limit.
    """
    if n < 2:   # base case
        return n
    return fib(n - 2) + fib(n - 1)  # recursive case


if __name__ == "__main__":
    print(fib(10))
    print(fib(50))
