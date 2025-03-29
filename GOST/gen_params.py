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
    print(f"Input parameters: p = {p}, a = {a}, b = {b}")
    F = GF(p)
    E = EllipticCurve(F, [a, b])
    if E.is_singular():
        raise ValueError("The curve is singular")
    j = E.j_invariant()
    print(f"j-invariant: {j}")
    N = E.order()
    print(f"Number of points (SEA): {N}")
    t = p + 1 - N
    print(f"Frobenius trace t: {t}")
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
    print(f"Total number of points m = {m}")
    print(f"j-invariant: {j}")
    factorization = factor(m)
    print(f"Factorization of m: {factorization}")
    q = max(f for f, e in factorization if is_prime(f))
    h = m // q 

    if len(factorization) == 1 and factorization[0][1] == 1:
        n = m
        h = 1
    else:
        n = q

    print(f"Group order n = {n}")
    print(f"Cofactor h = {m} / {n} = {h}")
    if h > 4:
        print("Warning: cofactor h > 4, may not be suitable for cryptography")
    if n < 2**128:
        print("Warning: order n is too small for security")
        return False

    return n, h


def find_base_point(p, a, b, q):
    F = GF(p)
    E = EllipticCurve(F, [a, b])
    m = E.order()
    h = m // q  # Cofactor
    if m != h * q:
        raise ValueError(f"m = {m} is not divisible by q = {q} with integer cofactor")

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


def check_security(p, a, b, q):
    F = GF(p)
    try:
        E = EllipticCurve(F, [a, b])
    except ValueError:
        return False, "Singular curve (4a^3 + 27b^2 ≡ 0 mod p)"

    m = E.order()
    if m == p:
        return False, f"Anomalous curve: m = {m} = p = {p}"

    n = m // q
    if m != n * q or n < 1:
        return False, f"Invalid cofactor: m = {m}, q = {q}, n = {n}"
    print(f"Cofactor n = {n}")

    j = E.j_invariant()
    if j == 0 or j == 1728:
        return False, f"Invalid J(E) = {j} (0 or 1728)"

    B = 31 if 2**128 < q < 2**256 else 131 if 2**508 < q < 2**512 else None
    if B is None:
        return False, f"q = {q} is not in the range 2^160 < q < 2^256 or 2^508 < q < 2^512"

    for t in range(1, B + 1):
        if pow(p, t, q) == 1:
            return False, f"MOV vulnerability: p^{t} ≡ 1 mod q"

    return True, "All checks passed"


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
        print(f"Result: m = {m},\nn = {q},\nh = {n}")
        print(f"Length: {q.bit_length()}")
        P = find_base_point(p, a, b, q)
        print(f"Base point P = {P}")
        print(f"Check: [q]P = {q * P}")

        is_safe, reason = check_security(p, a, b, q)
        print(f"Security: {is_safe}")
        print(f"Reason: {reason}")
        
        print(f"Time: {time.time() - t}")
        return p, a, b, m, q, P