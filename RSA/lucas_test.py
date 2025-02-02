import RSA.universal_functions as uni


def _lukas_extra_strong_params(n):
    P, Q, D = 3, 1, 5
    while True:
        g = uni.gcd(D, n)
        if g > 1 and g != n:
            return 0, 0, 0
        if jacobi_symbol(D, n) == -1:
            break
        P += 1
        D = P * P - 4
    return D, P, Q


def jacobi_symbol(k, n):
    k %= n  # деление по модулю
    if not k:
        return int(n == 1)  # (1, 1)
    if n == 1 or k == 1:
        return 1
    if uni.gcd(k, n) != 1:
        return 0

    result = 1
    while k != 0:
        while k % 2 == 0 and k > 0:
            k >>= 1  # / 2
            if n % 8 in (3, 5):
                result = -result
        k, n = n, k
        if k % 4 == n % 4 == 3:  # квадратичный закон взаимности
            result = -result
        k %= n
    return result


def _lucas_sequence(n, P, Q, k):
    D = P * P - 4 * Q
    if k == 0:
        return 0, 2, Q
    U = 1
    V = P
    Qk = Q
    b = k.bit_length()
    while b > 1:
        U = (U * V) % n
        V = (V * V - 2 * Qk) % n
        Qk *= Qk
        b -= 1
        if (k >> (b - 1)) & 1:
            U, V = U * P + V, V * P + U * D
            if U & 1:
                U += n
            if V & 1:
                V += n
            U, V = U >> 1, V >> 1
            Qk *= Q
        Qk %= n

    return U % n, V % n


def is_prime_lukas(n):
    D, P, Q = _lukas_extra_strong_params(n)
    if D == 0:
        return False

    s, k = n + 1, 0
    while s % 2 == 0:
        s, k = s >> 1, k + 1

    U, V = _lucas_sequence(n, P, Q, s)

    if U == 0 and V in (2, n - 2):
        return True
    for _ in range(1, k):
        if V == 0:
            return True
        V = (V * V - 2) % n
    return False
