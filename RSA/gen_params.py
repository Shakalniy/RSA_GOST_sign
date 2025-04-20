import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(__file__)))
from RSA import gen_keys
from RSA import gen_prime_nums as prime
import universal_functions as uni
import time


size = 1024


def gen_params():
    t = time.time()
    is_correct = False
    p, q = 0, 0
    while not is_correct:
        p = prime.gen_secure_prime_num(size)
        q = prime.gen_secure_prime_num(size)
        if max(p, q) - min(p, q) > 2**(size/4):
            is_correct = True

    n = p * q
    # print("Generated parameters:")
    # print("p = ", p)
    # print("q = ", q)
    # print("n = ", n)

    phi_n = (p - 1) * (q - 1)
    nod = uni.gcd(p-1, q-1)
    nok = phi_n // nod
    e, d = gen_keys.gen_keys(n, phi_n, nok)

    # print("Generated keys:")
    # print("e = ", e)
    # print("d = ", d)

    t = (time.time() - t).__round__(2)
    print("\nВремя выполнения программы:", t)

    return n, e, d
