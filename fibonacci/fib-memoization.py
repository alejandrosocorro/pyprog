from typing import Dict


memo: Dict[int, int] = {0: 0, 1: 1}  # base cases


def fib(n: int) -> int:
    if n not in memo:
        memo[n] = fib(n - 1) + fib(n - 2)
    return memo[n]


if __name__ == "__main__":
    print(fib(5))
    print(fib(50))
