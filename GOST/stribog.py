import numpy as np
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(__file__)))
from constants.stribog_constants import IV_512, IV_256, IV_512_HEX, IV_256_HEX, S_BOX, P_TABLE, L_MATRIX, C, block_size

# Вектор l_vec для умножения в поле Галуа
l_vec = [0x94, 0x20, 0x85, 0x10, 0xC2, 0xC0, 0x01, 0xFB]

# Таблица поиска для умножения в поле Галуа
GF_MUL_TABLE = np.zeros((256, 256), dtype=np.uint8)
for a in range(256):
    for b in range(256):
        r = 0
        aa, bb = a, b
        for _ in range(8):
            if bb & 1:
                r ^= aa
            high_bit = aa & 0x80
            aa = (aa << 1) & 0xFF
            if high_bit:
                aa ^= 0xC3  # Полином x^8 + x^6 + x^5 + x + 1
            bb >>= 1
        GF_MUL_TABLE[a][b] = r

def xor_transform(block1: bytes, block2: bytes) -> bytes:
    arr1 = np.frombuffer(block1, dtype=np.uint8)
    arr2 = np.frombuffer(block2, dtype=np.uint8)
    return (arr1 ^ arr2).tobytes()

def l_transform(block: bytes) -> bytes:
    result = bytearray(block)
    for _ in range(16):
        t = 0
        for i in range(block_size):
            t ^= GF_MUL_TABLE[result[i]][l_vec[i % 8]]
        result = bytes([t]) + result[:-1]
    return bytes(result)

def s_transform(block: bytes) -> bytes:
    arr = np.frombuffer(block, dtype=np.uint8)
    return bytes(S_BOX[b] for b in arr)

def p_transform(block: bytes) -> bytes:
    arr = np.frombuffer(block, dtype=np.uint8)
    return arr[P_TABLE].tobytes()

def lps_transform(block: bytes) -> bytes:
    return l_transform(p_transform(s_transform(block)))

def e_transform(K: bytes, m: bytes) -> bytes:
    state = xor_transform(m, K)
    for i in range(12):
        state = lps_transform(state)
        K = lps_transform(xor_transform(K, C[i]))
    return xor_transform(state, K)

def g_N(h: bytes, m: bytes, N: bytes) -> bytes:
    K = xor_transform(h, N)
    K = lps_transform(K)
    enc_block = e_transform(K, m)
    return xor_transform(xor_transform(enc_block, h), m)

def add_mod512(a: bytes, b: bytes) -> bytes:
    result = bytearray(block_size)
    carry = 0
    for i in range(block_size - 1, -1, -1):
        temp = a[i] + b[i] + carry
        result[i] = temp & 0xFF
        carry = temp >> 8
    return bytes(result)

def initialize_hash_function(bit_size: int):
    if bit_size == 512:
        h = IV_512
    elif bit_size == 256:
        h = IV_256
    else:
        raise ValueError("Допустимы только 256 или 512 бит.")
    N = bytes(block_size)
    Σ = bytes(block_size)
    return h, N, Σ

def pad_message(message: bytes) -> bytes:
    msg_len = len(message)
    pad_len = block_size - (msg_len % block_size)
    if pad_len == block_size:
        pad_len = 0
    padding = bytes([0x01]) + bytes(pad_len - 1)
    return message + padding if pad_len > 0 else message + bytes([0x01]) + bytes(block_size - 1)

def split_message_into_blocks(message: bytes):
    padded_message = pad_message(message)
    for i in range(0, len(padded_message), block_size):
        yield padded_message[i:i + block_size]

def process_message_block(h: bytes, N: bytes, Σ: bytes, blocks):
    block_bit_length = bytes([0] * (block_size - 2) + [0x02, 0x00])  # 512 бит
    for m in blocks:
        h = g_N(h, m, N)
        N = add_mod512(N, block_bit_length)
        Σ = add_mod512(Σ, m)
    return h, N, Σ

def final_transformation(h: bytes, Σ: bytes, N: bytes, bit_size: int) -> bytes:
    h = g_N(h, N, bytes(block_size))
    h = g_N(h, Σ, bytes(block_size))
    return h[32:] if bit_size == 256 else h

def start_stribog(M, size):
    if isinstance(M, str):
        M_bytes = M.encode('utf-8')
    else:
        M_bytes = M
    h, N, Σ = initialize_hash_function(size)
    blocks = split_message_into_blocks(M_bytes)
    h, N, Σ = process_message_block(h, N, Σ, blocks)
    h = final_transformation(h, Σ, N, size)
    return h.hex()
