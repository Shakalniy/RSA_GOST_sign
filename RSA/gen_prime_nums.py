import random
import sys
import RSA.lucas_test as lukas
import RSA.miller_test as miller
from constants.RSA_contstants import first_primes_list
sys.setrecursionlimit(3000)


def low_level_check(n):
    for divisor in first_primes_list:
        if n > divisor and n % divisor == 0:
            return False
    return True


def n_bit_random(n):
    return random.randrange(2 ** (n - 1) + 1, 2 ** n - 1)


def check_safe_prime(n):
    k = 2
    p = n * k + 1

    while True:
        if low_level_check(p):
            if miller.is_prime_miller(p, 1) and lukas.is_prime_lukas(p):
                return p

        k += 1
        p = n * k + 1


def check_prime(p):
    if miller.is_prime_miller(p, 1) and lukas.is_prime_lukas(p):
        return True
    return False


def gen_prime_num(size):
    while True:
        p = n_bit_random(size)
        if low_level_check(p):
            if not check_prime(p):
                continue
            else:
                return p


def gen_secure_prime_num(size):
    r1 = gen_prime_num(size)
    r = check_safe_prime(r1)
    p = check_safe_prime(r)

    return p
