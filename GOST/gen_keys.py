from random import randint


def gen_keys(q, P):
    d = randint(1, q-1)
    Q = d * P
    print(f"Закрытый ключ d = {d}")
    print(f"Открытый ключ Q = {Q}")
    return d, Q