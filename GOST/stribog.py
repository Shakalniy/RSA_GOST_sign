from GOST.constants.stribog_constants import IV_512, IV_256, IV_512_HEX, IV_256_HEX
import universal_function as uni


def initialize_hash_function(bit_size: int):
    """
    Инициализация хеш-функции ГОСТ 34.11-2018.
    :param bit_size: Размер выходного хеш-кода (256 или 512 бит).
    :return: Начальные значения h, N, Z
    """
    if bit_size == 512:
        h = IV_512  # Используем инициализационный вектор для 512 бит
    elif bit_size == 256:
        h = IV_256  # Используем инициализационный вектор для 256 бит
    else:
        raise ValueError("Допустимы только 256 или 512 бит.")

    N = bytes(64)  # Счетчик обработанных бит (изначально 0)
    Z = bytes(64)  # Контрольный блок (изначально 0)

    return h, N, Z


def start_stribog(M):
    size = uni.input_number("Выберите размер хеш-кода: ")
    h, N, Z = initialize_hash_function(size)
    pass


if __name__ == '__main__':
    M = 'dnfioqn833784rbth348ofbybg3q4rbyfiefghrweogbhrweifnwe0dfu2ef8nqwefn023qufnqwejfbewiofhweuf'
    start_stribog(M)
