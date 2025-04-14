# import struct
# import sys
# import os
# sys.path.append(os.path.dirname(os.path.dirname(__file__)))
#
#
# def sha256(message):
#     # Инициализация констант (первые 32 бита дробных частей кубических корней первых 64 простых чисел)
#     K = [
#         0x428a2f98, 0x71374491, 0xb5c0fbcf, 0xe9b5dba5, 0x3956c25b, 0x59f111f1, 0x923f82a4, 0xab1c5ed5,
#         0xd807aa98, 0x12835b01, 0x243185be, 0x550c7dc3, 0x72be5d74, 0x80deb1fe, 0x9bdc06a7, 0xc19bf174,
#         0xe49b69c1, 0xefbe4786, 0x0fc19dc6, 0x240ca1cc, 0x2de92c6f, 0x4a7484aa, 0x5cb0a9dc, 0x76f988da,
#         0x983e5152, 0xa831c66d, 0xb00327c8, 0xbf597fc7, 0xc6e00bf3, 0xd5a79147, 0x06ca6351, 0x14292967,
#         0x27b70a85, 0x2e1b2138, 0x4d2c6dfc, 0x53380d13, 0x650a7354, 0x766a0abb, 0x81c2c92e, 0x92722c85,
#         0xa2bfe8a1, 0xa81a664b, 0xc24b8b70, 0xc76c51a3, 0xd192e819, 0xd6990624, 0xf40e3585, 0x106aa070,
#         0x19a4c116, 0x1e376c08, 0x2748774c, 0x34b0bcb5, 0x391c0cb3, 0x4ed8aa4a, 0x5b9cca4f, 0x682e6ff3,
#         0x748f82ee, 0x78a5636f, 0x84c87814, 0x8cc70208, 0x90befffa, 0xa4506ceb, 0xbef9a3f7, 0xc67178f2
#     ]
#
#     # Инициализация хэш-значений (первые 32 бита дробных частей квадратных корней первых 8 простых чисел)
#     H = [
#         0x6a09e667, 0xbb67ae85, 0x3c6ef372, 0xa54ff53a,
#         0x510e527f, 0x9b05688c, 0x1f83d9ab, 0x5be0cd19
#     ]
#
#     # Преобразование входного сообщения в байты, если это строка
#     if isinstance(message, str):
#         message = message.encode('utf-8')
#
#     # Подготовка сообщения (добавление паддинга)
#     msg_length = len(message) * 8  # Длина в битах
#     message += b'\x80'  # Добавляем бит 1 (в байтах это 0x80)
#     # Добавляем нули, чтобы длина стала кратной 512 битам, минус 64 бита для длины
#     while (len(message) * 8) % 512 != 448:
#         message += b'\x00'
#     # Добавляем длину сообщения (64 бита) в big-endian
#     message += struct.pack('>Q', msg_length)
#
#     # Обработка сообщения блоками по 512 бит (64 байта)
#     for i in range(0, len(message), 64):
#         block = message[i:i + 64]
#         # Разбиваем блок на 16 слов по 32 бита
#         W = [0] * 64
#         for j in range(16):
#             W[j] = struct.unpack('>I', block[j * 4:j * 4 + 4])[0]
#
#         # Расширяем 16 слов до 64
#         for j in range(16, 64):
#             s0 = (right_rotate(W[j - 15], 7) ^ right_rotate(W[j - 15], 18) ^ (W[j - 15] >> 3))
#             s1 = (right_rotate(W[j - 2], 17) ^ right_rotate(W[j - 2], 19) ^ (W[j - 2] >> 10))
#             W[j] = (W[j - 16] + s0 + W[j - 7] + s1) & 0xFFFFFFFF
#
#         # Инициализация рабочих переменных
#         a, b, c, d, e, f, g, h = H
#
#         # Основной цикл сжатия
#         for j in range(64):
#             S1 = (right_rotate(e, 6) ^ right_rotate(e, 11) ^ right_rotate(e, 25))
#             ch = (e & f) ^ (~e & g)
#             temp1 = (h + S1 + ch + K[j] + W[j]) & 0xFFFFFFFF
#             S0 = (right_rotate(a, 2) ^ right_rotate(a, 13) ^ right_rotate(a, 22))
#             maj = (a & b) ^ (a & c) ^ (b & c)
#             temp2 = (S0 + maj) & 0xFFFFFFFF
#
#             h = g
#             g = f
#             f = e
#             e = (d + temp1) & 0xFFFFFFFF
#             d = c
#             c = b
#             b = a
#             a = (temp1 + temp2) & 0xFFFFFFFF
#
#         # Обновление хэш-значений
#         H[0] = (H[0] + a) & 0xFFFFFFFF
#         H[1] = (H[1] + b) & 0xFFFFFFFF
#         H[2] = (H[2] + c) & 0xFFFFFFFF
#         H[3] = (H[3] + d) & 0xFFFFFFFF
#         H[4] = (H[4] + e) & 0xFFFFFFFF
#         H[5] = (H[5] + f) & 0xFFFFFFFF
#         H[6] = (H[6] + g) & 0xFFFFFFFF
#         H[7] = (H[7] + h) & 0xFFFFFFFF
#
#     # Формирование итогового хэша
#     return ''.join(f'{h:08x}' for h in H)
#
#
# # Вспомогательная функция для правого вращения (rotate right)
# def right_rotate(n, d):
#     return (n >> d) | (n << (32 - d)) & 0xFFFFFFFF
#
#
# # Примеры использования
# if __name__ == "__main__":
#     import time
#     with open('picture_big.jpg', 'rb') as f:
#         message = f.read()
#     # Тестовые случаи
#     print(sha256(""))  # Хэш пустой строки
#     # Ожидается: e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855
#     print(sha256("abc"))
#     # Ожидается: ba7816bf8f01cfea414140de5dae2223b00361a396177a9cb410ff61f20015ad
#     print(sha256("The quick brown fox jumps over the lazy dog"))
#     print(sha256("ABCDEFGHIJKLMNOPQRASTUVWXYZabcdifghijklmnopqrstuvwxyz012"))
#     # Ожидается: d7a8fbb307d7809469ca9abcb0082e4f8d5651e46d3cdb762d02d0bf37c9e592
#     t = time.time()
#     print(sha256(message))
#     print(time.time() - t)


import struct
import sys
import os
import multiprocessing as mp
from functools import partial
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

def right_rotate(n, d):
    return (n >> d) | (n << (32 - d)) & 0xFFFFFFFF

def process_chunk(chunk, K, H_init):
    H = H_init.copy()
    # Подготовка сообщения (паддинг для каждого куска)
    msg_length = len(chunk) * 8
    chunk = bytearray(chunk)
    chunk.append(0x80)
    while (len(chunk) * 8) % 512 != 448:
        chunk.append(0x00)
    chunk.extend(struct.pack('>Q', msg_length))

    # Обработка блоками
    for i in range(0, len(chunk), 64):
        block = chunk[i:i + 64]
        W = [0] * 64
        for j in range(16):
            W[j] = (block[j*4] << 24) | (block[j*4+1] << 16) | (block[j*4+2] << 8) | block[j*4+3]

        for j in range(16, 64):
            s0 = right_rotate(W[j - 15], 7) ^ right_rotate(W[j - 15], 18) ^ (W[j - 15] >> 3)
            s1 = right_rotate(W[j - 2], 17) ^ right_rotate(W[j - 2], 19) ^ (W[j - 2] >> 10)
            W[j] = (W[j - 16] + s0 + W[j - 7] + s1) & 0xFFFFFFFF

        a, b, c, d, e, f, g, h = H

        for j in range(64):
            S1 = right_rotate(e, 6) ^ right_rotate(e, 11) ^ right_rotate(e, 25)
            ch = (e & f) ^ (~e & g)
            temp1 = (h + S1 + ch + K[j] + W[j]) & 0xFFFFFFFF
            S0 = right_rotate(a, 2) ^ right_rotate(a, 13) ^ right_rotate(a, 22)
            maj = (a & b) ^ (a & c) ^ (b & c)
            temp2 = (S0 + maj) & 0xFFFFFFFF

            h = g
            g = f
            f = e
            e = (d + temp1) & 0xFFFFFFFF
            d = c
            c = b
            b = a
            a = (temp1 + temp2) & 0xFFFFFFFF

        H[0] = (H[0] + a) & 0xFFFFFFFF
        H[1] = (H[1] + b) & 0xFFFFFFFF
        H[2] = (H[2] + c) & 0xFFFFFFFF
        H[3] = (H[3] + d) & 0xFFFFFFFF
        H[4] = (H[4] + e) & 0xFFFFFFFF
        H[5] = (H[5] + f) & 0xFFFFFFFF
        H[6] = (H[6] + g) & 0xFFFFFFFF
        H[7] = (H[7] + h) & 0xFFFFFFFF

    return H

def sha256(message):
    # Инициализация констант
    K = [
        0x428a2f98, 0x71374491, 0xb5c0fbcf, 0xe9b5dba5, 0x3956c25b, 0x59f111f1, 0x923f82a4, 0xab1c5ed5,
        0xd807aa98, 0x12835b01, 0x243185be, 0x550c7dc3, 0x72be5d74, 0x80deb1fe, 0x9bdc06a7, 0xc19bf174,
        0xe49b69c1, 0xefbe4786, 0x0fc19dc6, 0x240ca1cc, 0x2de92c6f, 0x4a7484aa, 0x5cb0a9dc, 0x76f988da,
        0x983e5152, 0xa831c66d, 0xb00327c8, 0xbf597fc7, 0xc6e00bf3, 0xd5a79147, 0x06ca6351, 0x14292967,
        0x27b70a85, 0x2e1b2138, 0x4d2c6dfc, 0x53380d13, 0x650a7354, 0x766a0abb, 0x81c2c92e, 0x92722c85,
        0xa2bfe8a1, 0xa81a664b, 0xc24b8b70, 0xc76c51a3, 0xd192e819, 0xd6990624, 0xf40e3585, 0x106aa070,
        0x19a4c116, 0x1e376c08, 0x2748774c, 0x34b0bcb5, 0x391c0cb3, 0x4ed8aa4a, 0x5b9cca4f, 0x682e6ff3,
        0x748f82ee, 0x78a5636f, 0x84c87814, 0x8cc70208, 0x90befffa, 0xa4506ceb, 0xbef9a3f7, 0xc67178f2
    ]

    # Инициализация хэш-значений
    H_init = [
        0x6a09e667, 0xbb67ae85, 0x3c6ef372, 0xa54ff53a,
        0x510e527f, 0x9b05688c, 0x1f83d9ab, 0x5be0cd19
    ]

    # Преобразование входного сообщения в байты
    if isinstance(message, str):
        message = message.encode('utf-8')

    # Для маленьких сообщений используем стандартный SHA-256
    if len(message) < 1024:
        return standard_sha256(message)

    # Разделение на куски
    num_cores = mp.cpu_count()
    chunk_size = (len(message) + num_cores - 1) // num_cores
    chunks = [message[i:i + chunk_size] for i in range(0, len(message), chunk_size)]

    # Параллельная обработка
    with mp.Pool(num_cores) as pool:
        results = pool.map(partial(process_chunk, K=K, H_init=H_init), chunks)

    # Комбинирование результатов (хэшируем результаты вместе)
    combined = bytearray()
    for res in results:
        for h in res:
            combined.extend(struct.pack('>I', h))
    return standard_sha256(combined)

def standard_sha256(message):
    K = [
        0x428a2f98, 0x71374491, 0xb5c0fbcf, 0xe9b5dba5, 0x3956c25b, 0x59f111f1, 0x923f82a4, 0xab1c5ed5,
        0xd807aa98, 0x12835b01, 0x243185be, 0x550c7dc3, 0x72be5d74, 0x80deb1fe, 0x9bdc06a7, 0xc19bf174,
        0xe49b69c1, 0xefbe4786, 0x0fc19dc6, 0x240ca1cc, 0x2de92c6f, 0x4a7484aa, 0x5cb0a9dc, 0x76f988da,
        0x983e5152, 0xa831c66d, 0xb00327c8, 0xbf597fc7, 0xc6e00bf3, 0xd5a79147, 0x06ca6351, 0x14292967,
        0x27b70a85, 0x2e1b2138, 0x4d2c6dfc, 0x53380d13, 0x650a7354, 0x766a0abb, 0x81c2c92e, 0x92722c85,
        0xa2bfe8a1, 0xa81a664b, 0xc24b8b70, 0xc76c51a3, 0xd192e819, 0xd6990624, 0xf40e3585, 0x106aa070,
        0x19a4c116, 0x1e376c08, 0x2748774c, 0x34b0bcb5, 0x391c0cb3, 0x4ed8aa4a, 0x5b9cca4f, 0x682e6ff3,
        0x748f82ee, 0x78a5636f, 0x84c87814, 0x8cc70208, 0x90befffa, 0xa4506ceb, 0xbef9a3f7, 0xc67178f2
    ]

    H = [
        0x6a09e667, 0xbb67ae85, 0x3c6ef372, 0xa54ff53a,
        0x510e527f, 0x9b05688c, 0x1f83d9ab, 0x5be0cd19
    ]

    if isinstance(message, str):
        message = message.encode('utf-8')

    msg_length = len(message) * 8
    message = bytearray(message)
    message.append(0x80)
    while (len(message) * 8) % 512 != 448:
        message.append(0x00)
    message.extend(struct.pack('>Q', msg_length))

    for i in range(0, len(message), 64):
        block = message[i:i + 64]
        W = [0] * 64
        for j in range(16):
            W[j] = (block[j*4] << 24) | (block[j*4+1] << 16) | (block[j*4+2] << 8) | block[j*4+3]

        for j in range(16, 64):
            s0 = right_rotate(W[j - 15], 7) ^ right_rotate(W[j - 15], 18) ^ (W[j - 15] >> 3)
            s1 = right_rotate(W[j - 2], 17) ^ right_rotate(W[j - 2], 19) ^ (W[j - 2] >> 10)
            W[j] = (W[j - 16] + s0 + W[j - 7] + s1) & 0xFFFFFFFF

        a, b, c, d, e, f, g, h = H

        for j in range(64):
            S1 = right_rotate(e, 6) ^ right_rotate(e, 11) ^ right_rotate(e, 25)
            ch = (e & f) ^ (~e & g)
            temp1 = (h + S1 + ch + K[j] + W[j]) & 0xFFFFFFFF
            S0 = right_rotate(a, 2) ^ right_rotate(a, 13) ^ right_rotate(a, 22)
            maj = (a & b) ^ (a & c) ^ (b & c)
            temp2 = (S0 + maj) & 0xFFFFFFFF

            h = g
            g = f
            f = e
            e = (d + temp1) & 0xFFFFFFFF
            d = c
            c = b
            b = a
            a = (temp1 + temp2) & 0xFFFFFFFF

        H[0] = (H[0] + a) & 0xFFFFFFFF
        H[1] = (H[1] + b) & 0xFFFFFFFF
        H[2] = (H[2] + c) & 0xFFFFFFFF
        H[3] = (H[3] + d) & 0xFFFFFFFF
        H[4] = (H[4] + e) & 0xFFFFFFFF
        H[5] = (H[5] + f) & 0xFFFFFFFF
        H[6] = (H[6] + g) & 0xFFFFFFFF
        H[7] = (H[7] + h) & 0xFFFFFFFF

    result = bytearray(32)
    for i in range(8):
        result[i * 4] = (H[i] >> 24) & 0xFF
        result[i * 4 + 1] = (H[i] >> 16) & 0xFF
        result[i * 4 + 2] = (H[i] >> 8) & 0xFF
        result[i * 4 + 3] = H[i] & 0xFF
    return bytes(result)

if __name__ == "__main__":
    import time
    with open('picture_big.jpg', 'rb') as f:
        message = f.read()
    # Тестовые случаи
    print(sha256("").hex())  # Ожидается: e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855
    print(sha256("abc").hex())  # Ожидается: ba7816bf8f01cfea414140de5dae2223b00361a396177a9cb410ff61f20015ad
    print(sha256("The quick brown fox jumps over the lazy dog").hex())
    print(sha256("ABCDEFGHIJKLMNOPQRASTUVWXYZabcdifghijklmnopqrstuvwxyz012").hex())
    t = time.time()
    hash_result = sha256(message).hex()
    print(hash_result)
    print(f"Время выполнения: {time.time() - t:.5f} сек")