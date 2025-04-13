import numpy as np
from numba import njit
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(__file__)))
from constants.stribog_constants import IV_512, IV_256, S_BOX, P_TABLE, C, block_size

# Преобразуем константы в NumPy-массивы
S_BOX = np.array(S_BOX, dtype=np.uint8)
P_TABLE = np.array(P_TABLE, dtype=np.uint8)
l_vec = np.array([0x94, 0x20, 0x85, 0x10, 0xC2, 0xC0, 0x01, 0xFB], dtype=np.uint8)

# Таблица умножения в поле Галуа
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
                aa ^= 0xC3
            bb >>= 1
        GF_MUL_TABLE[a][b] = r

@njit
def l_transform_inner(result, gf_table, l_vec, block_size):
    for _ in range(16):
        t = 0
        for i in range(block_size):
            t ^= gf_table[result[i]][l_vec[i % 8]]
        result = np.roll(result, -1)
        result[0] = t
    return result

@njit
def e_transform_inner(state, K, s_box, p_table, gf_table, l_vec, block_size, C):
    for i in range(12):
        state = s_box[state]
        state = state[p_table]
        state = l_transform_inner(state, gf_table, l_vec, block_size)
        K = K ^ np.frombuffer(C[i], dtype=np.uint8)
        K = s_box[K]
        K = K[p_table]
        K = l_transform_inner(K, gf_table, l_vec, block_size)
    return state ^ K

@njit
def g_N_inner(h, m, N, s_box, p_table, gf_table, l_vec, block_size, C):
    K = h ^ N
    K = s_box[K]
    K = K[p_table]
    K = l_transform_inner(K, gf_table, l_vec, block_size)
    enc_block = e_transform_inner(m, K, s_box, p_table, gf_table, l_vec, block_size, C)
    return (enc_block ^ h) ^ m

@njit
def add_mod512_inner(a, b):
    result = np.zeros(64, dtype=np.uint8)
    carry = 0
    for i in range(63, -1, -1):
        temp = a[i] + b[i] + carry
        result[i] = temp & 0xFF
        carry = temp >> 8
    return result

@njit
def process_message_block_inner(h, N, Σ, blocks, block_bit_length, s_box, p_table, gf_table, l_vec, block_size, C):
    for m in blocks:
        h = g_N_inner(h, m, N, s_box, p_table, gf_table, l_vec, block_size, C)
        N = add_mod512_inner(N, block_bit_length)
        Σ = add_mod512_inner(Σ, m)
    return h, N, Σ

def xor_transform(block1: bytes, block2: bytes) -> bytes:
    arr1 = np.frombuffer(block1, dtype=np.uint8)
    arr2 = np.frombuffer(block2, dtype=np.uint8)
    return (arr1 ^ arr2).tobytes()

def s_transform(block: bytes) -> bytes:
    arr = np.frombuffer(block, dtype=np.uint8)
    return bytes(S_BOX[arr])

def p_transform(block: bytes) -> bytes:
    arr = np.frombuffer(block, dtype=np.uint8)
    return arr[P_TABLE].tobytes()

def lps_transform(block: bytes) -> bytes:
    arr = np.frombuffer(block, dtype=np.uint8)
    result = l_transform_inner(S_BOX[arr][P_TABLE], GF_MUL_TABLE, l_vec, block_size)
    return bytes(result)

def e_transform(K: bytes, m: bytes) -> bytes:
    state = np.frombuffer(xor_transform(m, K), dtype=np.uint8)
    K_arr = np.frombuffer(K, dtype=np.uint8)
    result = e_transform_inner(state, K_arr, S_BOX, P_TABLE, GF_MUL_TABLE, l_vec, block_size, C)
    return bytes(result)

def g_N(h: bytes, m: bytes, N: bytes) -> bytes:
    h_arr = np.frombuffer(h, dtype=np.uint8)
    m_arr = np.frombuffer(m, dtype=np.uint8)
    N_arr = np.frombuffer(N, dtype=np.uint8)
    result = g_N_inner(h_arr, m_arr, N_arr, S_BOX, P_TABLE, GF_MUL_TABLE, l_vec, block_size, C)
    return bytes(result)

def add_mod512(a: bytes, b: bytes) -> bytes:
    a_arr = np.frombuffer(a, dtype=np.uint8)
    b_arr = np.frombuffer(b, dtype=np.uint8)
    result = add_mod512_inner(a_arr, b_arr)
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
    if msg_len % block_size == 0:
        return message
    else:
        pad_len = block_size - (msg_len % block_size)
        if pad_len == block_size:
            pad_len = 0
        padding = bytes([0x01]) + bytes(pad_len - 1)
        return message + padding if pad_len > 0 else message + bytes([0x01]) + bytes(block_size - 1)

def split_message_into_blocks(message: bytes):
    padded_message = pad_message(message)
    # Преобразуем в массив NumPy для Numba
    num_blocks = len(padded_message) // block_size
    arr = np.frombuffer(padded_message, dtype=np.uint8).reshape(num_blocks, block_size)
    return arr

def process_message_block(h: bytes, N: bytes, Σ: bytes, blocks):
    block_bit_length = np.frombuffer(bytes([0] * (block_size - 2) + [0x02, 0x00]), dtype=np.uint8)
    h_arr = np.frombuffer(h, dtype=np.uint8)
    N_arr = np.frombuffer(N, dtype=np.uint8)
    Σ_arr = np.frombuffer(Σ, dtype=np.uint8)
    h_arr, N_arr, Σ_arr = process_message_block_inner(
        h_arr, N_arr, Σ_arr, blocks, block_bit_length, S_BOX, P_TABLE, GF_MUL_TABLE, l_vec, block_size, C
    )
    return bytes(h_arr), bytes(N_arr), bytes(Σ_arr)

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
