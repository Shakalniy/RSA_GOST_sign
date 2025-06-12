import sys
import os
import random
import math
import time
original_dir = os.getcwd()
sys.path.append(os.path.dirname(os.path.dirname(__file__)))
import universal_functions as uni
from constants.RSA_contstants import first_primes_list
from RSA.gen_prime_nums import gen_prime_num
from sage.all import GF, EllipticCurve, factor, is_prime
os.chdir(original_dir)


def sea_point_count(p, a, b):
    print(f"Входные параметры: p = {p}, a = {a}, b = {b}")
    F = GF(p)
    E = EllipticCurve(F, [a, b])
    if E.is_singular():
        raise ValueError("Кривая сингулярна")
    j = E.j_invariant()
    print(f"j-инвариант: {j}")
    N = E.order()
    print(f"Количество точек (SEA): {N}")
    t = p + 1 - N
    print(f"След Фробениуса t: {t}")
    return N


def gen_elliptic_curve_params(p):
    D = 0
    j = 0
    a, b = 0, 0
    while D == 0 or (j == 0 or j == 1728):
        a = random.randrange(1, p - 1)
        b = random.randrange(1, p - 1)
        D = (4 * uni.power(a, 3, p) + 27 * uni.power(b, 2, p)) % p
        D_obr = uni.gcd_extended(D, p)
        j = ((1728 * 4 * uni.power(a, 3, p)) * D_obr[2]) % p
    return a, b, j


def chose_primes(p):
    lim = 4 * (math.isqrt(p) + 1)
    prod = 1
    for i, prime in enumerate(first_primes_list):
        prod *= prime
        if prod > lim:
            return first_primes_list[:i]
    return first_primes_list


def check_curve_order(m, j):
    print(f"Общее количество точек m = {m}")
    print(f"j-инвариант: {j}")
    factorization = factor(m)
    print(f"Факторизация числа m: {factorization}")
    q = max(f for f, e in factorization if is_prime(f))
    h = m // q 

    if len(factorization) == 1 and factorization[0][1] == 1:
        n = m
        h = 1
    else:
        n = q

    print(f"Порядок группы n = {n}")
    print(f"Сомножитель h = {m} / {n} = {h}")
    if n < 2**128:
        print("Порядок n слишком мал.")
        return False

    return n, h


def find_base_point(p, a, b, q):
    F = GF(p)
    E = EllipticCurve(F, [a, b])
    m = E.order()
    h = m // q  # сомножитель
    if m != h * q:
        raise ValueError(f"m = {m} не делится на q = {q} с целым сомножителем")

    while True:
        x = F.random_element()
        z = x**3 + a*x + b
        if not z.is_square():
            continue
        y = z.sqrt()
        P = E(x, y)
        if P == E(0):
            continue
        Q = h * P
        if Q == E(0):
            continue
        if q * Q == E(0):
            return Q


def gen_params():
    while True:
        t = time.time()
        p = gen_prime_num(256)
        a, b, j = gen_elliptic_curve_params(p)
        m = sea_point_count(p, a, b)
        if p == m:
            print("p == m")
            continue
        res = check_curve_order(m, j)
        if not res:
            continue
        q, n = res
        print(f"Результат: m = {m},\nn = {q},\nh = {n}")
        print(f"Длина: {q.bit_length()}")
        P = find_base_point(p, a, b, q)
        print(f"Базовая точка P = {P}")
        print(f"Проверка: [q]P = {q * P}")

        t = (time.time() - t).__round__(2)
        print("\nВремя выполнения программы:", t)
        return p, a, b, m, q, P
