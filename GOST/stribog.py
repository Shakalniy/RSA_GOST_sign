# from GOST.constants.stribog_constants import IV_512, IV_256, IV_512_HEX, IV_256_HEX, S_BOX, P_TABLE, L_MATRIX, C
from constants.stribog_constants import IV_512, IV_256, IV_512_HEX, IV_256_HEX, S_BOX, P_TABLE, L_MATRIX, C


def initialize_hash_function(bit_size: int):
    if bit_size == 512:
        h = IV_512
    elif bit_size == 256:
        h = IV_256
    else:
        raise ValueError("Допустимы только 256 или 512 бит.")
    
    N = bytes(64)
    Z = bytes(64)
    return h, N, Z


def split_message_into_blocks(message: bytes) -> list:
    block_size = 64
    length_in_bits = len(message) * 8
    message += b'\x80'
    padding_size = (block_size - (len(message) % block_size)) % block_size
    message += b'\x00' * padding_size
    message += length_in_bits.to_bytes(64, 'little')
    return [message[i:i+block_size] for i in range(0, len(message), block_size)]


def xor_transform(block1: bytes, block2: bytes) -> bytes:
    if not isinstance(block1, (bytes, bytearray)) or not isinstance(block2, (bytes, bytearray)):
        raise TypeError("Both arguments must be bytes or bytearray")
    return bytes(a ^ b for a, b in zip(block1, block2))


def s_transform(block: bytes) -> bytes:
    return bytes(S_BOX[b] for b in block)


def p_transform(block: bytes) -> bytes:
    return bytes(block[P_TABLE[i]] for i in range(len(block)))


def l_transform(block: bytes) -> bytes:
    """ L-преобразование """
    result = bytearray(64)  # Результирующий блок из 64 байт
    for i in range(8):  # Перебираем каждый байт входного блока (8 байт)
        for j in range(8):  # Перебираем каждый бит в текущем байте
            if (block[i] >> j) & 1:  # Если j-й бит i-го байта равен 1
                # Добавляем соответствующую строку матрицы L к результату
                if j < len(L_MATRIX) and i < len(L_MATRIX[j]):  # Проверяем границы
                    l_value = L_MATRIX[j][i].to_bytes(8, 'big')  # Преобразуем число в байты
                    for k in range(8):  # Перебираем все 8 байт строки матрицы
                        result[k + i * 8] ^= l_value[k]
    return bytes(result)


def lps_transform(block):
    return l_transform(p_transform(s_transform(block)))


def e_transform(K, m):
    state = xor_transform(m, K)
    for i in range(12):
        state = lps_transform(state)
        K = lps_transform(xor_transform(K, C[i]))
    return xor_transform(state, K)


def process_message_block(h, N, Z, blocks):
    for block in blocks:
        K = lps_transform(xor_transform(h, N))
        enc_block = e_transform(K, block)
        h = xor_transform(enc_block, xor_transform(h, block))
        N = (int.from_bytes(N, 'big') + 512).to_bytes(64, 'big')
        Z = xor_transform(Z, block)
    return h, N, Z


def final_transformation(h, Z):
    return lps_transform(xor_transform(h, Z))


def start_stribog(M, size):
    h, N, Z = initialize_hash_function(size)
    blocks = split_message_into_blocks(M.encode())
    h, N, Z = process_message_block(h, N, Z, blocks)
    h = final_transformation(h, Z)
    return h[:32] if size == 256 else h


if __name__ == '__main__':
    M = 'abc'
    h_512 = start_stribog(M, 512)
    print(h_512.hex())
    h_256 = start_stribog(M, 256)
    print(h_256.hex())
