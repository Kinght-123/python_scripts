import time
import sys

import redis

# 将递归深度限制设置为2000
sys.setrecursionlimit(2000)


def recur(n):
    if n == 1:
        return 1
    else:
        return n + recur(n - 1)


def tail_recur(n, res):
    if n == 0:
        return res
    return tail_recur(n - 1, n + res)


def fib1(n, a=0, b=1):
    if n == 1:
        return a
    if n == 2:
        return b
    return fib1(n - 1, b, a + b)


def fib(n: int) -> int:
    """斐波那契数列：递归"""
    # 终止条件 f(1) = 0, f(2) = 1
    if n == 1 or n == 2:
        return n - 1
    # 递归调用 f(n) = f(n-1) + f(n-2)
    res = fib(n - 1) + fib(n - 2)
    # 返回结果 f(n)
    return res




if __name__ == '__main__':

    print(fib(5))
    print(fib1(5))
    # a = time.time()
    # print(f'res: {recur(1500)}')
    # print(f'time: {time.time() - a}s')
    #
    # c =time.time()
    # print(f'res: {tail_recur(1500, 0)}')
    # print(f'time: {time.time() - c}s')
