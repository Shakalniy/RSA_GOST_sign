import numpy as np
from numba import njit, uint32, uint8

# Функция для правого циклического сдвига
@njit(uint32(uint32, uint32))
def right_rotate(x: uint32, n: uint32) -> uint32:
    """Выполняет циклический сдвиг вправо для 32-битного числа."""
    return ((x >> n) | (x << (32 - n))) & 0xFFFFFFFF

# Функция сжатия блока
@njit
def compress_block(block: uint8[:], H: uint32[:], K: uint32[:]):
    """Обрабатывает один 64-байтовый блок сообщения и обновляет хэш."""
    # Инициализация массива W
    W = np.zeros(64, dtype=np.uint32)

    # Преобразование байтов в слова
    for j in range(16):
        j4 = j * 4
        W[j] = (uint32(block[j4]) << 24) | (uint32(block[j4 + 1]) << 16) | \
               (uint32(block[j4 + 2]) << 8) | uint32(block[j4 + 3])

    # Расширение слов
    for j in range(16, 64):
        w15, w2 = W[j - 15], W[j - 2]
        s0 = right_rotate(w15, 7) ^ right_rotate(w15, 18) ^ (w15 >> 3)
        s1 = right_rotate(w2, 17) ^ right_rotate(w2, 19) ^ (w2 >> 10)
        W[j] = uint32(W[j - 16] + s0 + W[j - 7] + s1) & 0xFFFFFFFF

    # Инициализация рабочих переменных
    a, b, c, d, e, f, g, h = [uint32(H[i]) for i in range(8)]

    # Основной цикл сжатия
    for j in range(64):
        S1 = right_rotate(e, 6) ^ right_rotate(e, 11) ^ right_rotate(e, 25)
        # Используем XOR вместо ~ для избежания проблем с типами
        not_e = uint32(0xFFFFFFFF ^ e)
        ch = uint32(e & f) ^ uint32(not_e & g)
        temp1 = uint32(h + S1 + ch + K[j] + W[j]) & 0xFFFFFFFF
        S0 = right_rotate(a, 2) ^ right_rotate(a, 13) ^ right_rotate(a, 22)
        maj = uint32(a & b) ^ uint32(a & c) ^ uint32(b & c)
        temp2 = uint32(S0 + maj) & 0xFFFFFFFF

        h, g, f = g, f, e
        e = uint32(d + temp1) & 0xFFFFFFFF
        d, c, b = c, b, a
        a = uint32(temp1 + temp2) & 0xFFFFFFFF

    # Обновление хэша
    H[0] = uint32(H[0] + a) & 0xFFFFFFFF
    H[1] = uint32(H[1] + b) & 0xFFFFFFFF
    H[2] = uint32(H[2] + c) & 0xFFFFFFFF
    H[3] = uint32(H[3] + d) & 0xFFFFFFFF
    H[4] = uint32(H[4] + e) & 0xFFFFFFFF
    H[5] = uint32(H[5] + f) & 0xFFFFFFFF
    H[6] = uint32(H[6] + g) & 0xFFFFFFFF
    H[7] = uint32(H[7] + h) & 0xFFFFFFFF

@njit
def sha256_inner(padded: uint8[:], padded_len: int, K: uint32[:]) -> uint32[:]:
    """Вычисляет хэш SHA-256 для подготовленного сообщения."""
    H = np.array([
        0x6a09e667, 0xbb67ae85, 0x3c6ef372, 0xa54ff53a,
        0x510e527f, 0x9b05688c, 0x1f83d9ab, 0x5be0cd19
    ], dtype=np.uint32)

    for i in range(0, padded_len, 64):
        block = padded[i:i + 64]
        compress_block(block, H, K)

    return H

def sha256(message):
    """Вычисляет SHA-256 хэш сообщения."""
    K = np.array([
        0x428a2f98, 0x71374491, 0xb5c0fbcf, 0xe9b5dba5, 0x3956c25b, 0x59f111f1, 0x923f82a4, 0xab1c5ed5,
        0xd807aa98, 0x12835b01, 0x243185be, 0x550c7dc3, 0x72be5d74, 0x80deb1fe, 0x9bdc06a7, 0xc19bf174,
        0xe49b69c1, 0xefbe4786, 0x0fc19dc6, 0x240ca1cc, 0x2de92c6f, 0x4a7484aa, 0x5cb0a9dc, 0x76f988da,
        0x983e5152, 0xa831c66d, 0xb00327c8, 0xbf597fc7, 0xc6e00bf3, 0xd5a79147, 0x06ca6351, 0x14292967,
        0x27b70a85, 0x2e1b2138, 0x4d2c6dfc, 0x53380d13, 0x650a7354, 0x766a0abb, 0x81c2c92e, 0x92722c85,
        0xa2bfe8a1, 0xa81a664b, 0xc24b8b70, 0xc76c51a3, 0xd192e819, 0xd6990624, 0xf40e3585, 0x106aa070,
        0x19a4c116, 0x1e376c08, 0x2748774c, 0x34b0bcb5, 0x391c0cb3, 0x4ed8aa4a, 0x5b9cca4f, 0x682e6ff3,
        0x748f82ee, 0x78a5636f, 0x84c87814, 0x8cc70208, 0x90befffa, 0xa4506ceb, 0xbef9a3f7, 0xc67178f2
    ], dtype=np.uint32)

    if isinstance(message, str):
        message = message.encode('utf-8')
    msg_length = len(message)

    # Паддинг
    padded_len = msg_length + 1 + 8
    while (padded_len * 8) % 512 != 0:
        padded_len += 1
    padded = bytearray(padded_len)
    padded[:msg_length] = message
    padded[msg_length] = 0x80
    bit_length = msg_length * 8
    for i in range(8):
        padded[padded_len - 8 + i] = (bit_length >> (56 - i * 8)) & 0xFF

    padded_arr = np.frombuffer(padded, dtype=np.uint8)
    H = sha256_inner(padded_arr, padded_len, K)

    result = bytearray(32)
    for i in range(8):
        i4 = i * 4
        result[i4] = (H[i] >> 24) & 0xFF
        result[i4 + 1] = (H[i] >> 16) & 0xFF
        result[i4 + 2] = (H[i] >> 8) & 0xFF
        result[i4 + 3] = H[i] & 0xFF
    return bytes(result)


if __name__ == "__main__":
    import time
    import hashlib

    # Функция для тестирования
    def test_sha256(input_data, expected_hex):
        result = sha256(input_data)
        hex_result = result.hex()
        print(f"Вход: {input_data!r}")
        print(f"Результат (bytes): {result}")
        print(f"Результат (hex): {hex_result}")
        print(f"Ожидаемый (hex): {expected_hex}")
        print(f"Совпадает с hashlib: {hashlib.sha256(input_data.encode() if isinstance(input_data, str) else input_data).hexdigest() == hex_result}")
        print()

    # Тестовые примеры
    test_sha256("", "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855")
    test_sha256("abc", "ba7816bf8f01cfea414140de5dae2223b00361a396177a9cb410ff61f20015ad")
    test_sha256("The quick brown fox jumps over the lazy dog", "d7a8fbb307d7809469ca9abcb0082e4f8d5651e46d3cdb762d02d0bf37c9e592")
    test_sha256("ABCDEFGHIJKLMNOPQRASTUVWXYZabcdifghijklmnopqrstuvwxyz012", "8da42cf08db5e96a775d96202fd2267316604e5ecc0cdb2d92ff4d60c65d3e36")

    # Тест на большом файле
    with open('picture_big.jpg', 'rb') as f:
        message = f.read()
    t = time.time()
    hash_result = sha256(message)
    print(f"Хэш для picture_big.jpg (hex): {hash_result.hex()}")
    print(f"Время выполнения: {time.time() - t:.5f} сек")

    # Сравнение с hashlib
    t = time.time()
    hashlib_result = hashlib.sha256(message).digest()
    print(f"Время hashlib: {time.time() - t:.5f} сек")
    print(f"Совпадает с hashlib: {hash_result == hashlib_result}")
