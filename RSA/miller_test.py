import random
import universal_functions as uni


def is_prime_miller(n, k):
    d = n - 1
    while d % 2 == 0:
        d //= 2
    for i in range(k):
        if not miller_test(d, n):
            return False
    return True


def miller_test(d, n):
    a = 2 + random.randint(1, n - 4)
    x = uni.power(a, d, n)
    if x == 1 or x == n - 1:
        return True
    while d != n - 1:
        x = (x * x) % n
        d *= 2
        if x == 1:
            return False
        if x == n - 1:
            return True
    return False
