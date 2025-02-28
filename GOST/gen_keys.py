from random import randint


def gen_keys(q, P):
    d = randint(1, q-1)
    Q = d * P
    print(f"Private key d = {d}")
    print(f"Public key Q = {Q}")
    return d, Q