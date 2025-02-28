from constants.stribog_constants import IV_512, IV_256, IV_512_HEX, IV_256_HEX, S_BOX, P_TABLE, L_MATRIX, C, block_size

def xor_transform(block1: bytes, block2: bytes) -> bytes:
    if not isinstance(block1, (bytes, bytearray)) or not isinstance(block2, (bytes, bytearray)):
        raise TypeError("Both arguments must be bytes or bytearray")
    return bytes(a ^ b for a, b in zip(block1, block2))

def gf_mul(a: int, b: int) -> int:
    r = 0
    for _ in range(8):
        if b & 1:
            r ^= a
        high_bit = a & 0x80
        a = (a << 1) & 0xFF
        if high_bit:
            a ^= 0xC3
        b >>= 1
    return r

l_vec = [0x94, 0x20, 0x85, 0x10, 0xC2, 0xC0, 0x01, 0xFB]

def R(state: bytes) -> bytes:
    t = 0
    for i in range(block_size):
        t ^= gf_mul(state[i], l_vec[i % 8])
    return bytes([t]) + state[:-1]

def l_transform(block: bytes) -> bytes:
    for _ in range(16):
        block = R(block)
    return bytes(block)

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
    pad_len = block_size - (len(message) % block_size)
    if pad_len == 0:
        pad_len = block_size
    return message + bytes([0x01]) + bytes(pad_len - 1)

def split_message_into_blocks(message: bytes) -> list:
    padded_message = pad_message(message)
    blocks = []
    for i in range(0, len(padded_message), block_size):
        blocks.append(padded_message[i:i + block_size])
    return blocks

def s_transform(block: bytes) -> bytes:
    return bytes(S_BOX[b] for b in block)

def p_transform(block: bytes) -> bytes:
    return bytes(block[P_TABLE[i]] for i in range(len(block)))

def lps_transform(block):
    return l_transform(p_transform(s_transform(block)))

def e_transform(K, m):
    state = xor_transform(m, K)
    for i in range(12):
        state = lps_transform(state)
        K = lps_transform(xor_transform(K, C[i]))
    return xor_transform(state, K)

def g_N(h, m, N):
    K = xor_transform(h, N)
    K = lps_transform(K)
    enc_block = e_transform(K, m)
    return xor_transform(xor_transform(enc_block, h), m)

def add_mod512(a: bytes, b: bytes) -> bytes:
    a_int = int.from_bytes(a, 'big')
    b_int = int.from_bytes(b, 'big')
    s_int = (a_int + b_int) % (1 << (block_size * 8))
    return s_int.to_bytes(block_size, 'big')

def process_message_block(h: bytes, N: bytes, Σ: bytes, blocks: list) -> (bytes, bytes, bytes):
    block_bit_length = (block_size * 8).to_bytes(block_size, 'big')
    for m in blocks:
        h = g_N(h, m, N)
        N = add_mod512(N, block_bit_length)
        Σ = add_mod512(Σ, m)
    return h, N, Σ

def final_transformation(h, Σ, N, bit_size):
    h = g_N(h, N, bytes(block_size))
    h = g_N(h, Σ, bytes(block_size))
    return h[32:] if bit_size == 256 else h

def start_stribog(M, size):
    M_bytes = M.encode('utf-8')
    h, N, Σ = initialize_hash_function(size)
    blocks = split_message_into_blocks(M_bytes)
    h, N, Σ = process_message_block(h, N, Σ, blocks)
    h = final_transformation(h, Σ, N, size)
    return h.hex()