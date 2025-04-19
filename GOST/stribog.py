import ctypes
import os
import time
import sys

# Путь к библиотеке
if os.name == 'nt':  # Windows
    lib_path = './stribog.dll'
else:  # Linux
    lib_path = './GOST/libstribog.so'

# Проверка существования файла
if not os.path.exists(lib_path):
    print(f"Ошибка: Библиотека не найдена по пути: {lib_path}")
    sys.exit(1)

try:
    # Загрузка библиотеки
    lib = ctypes.CDLL(lib_path)
except OSError as e:
    print(f"Ошибка загрузки библиотеки: {e}")
    sys.exit(1)

# Определение сигнатуры функции
lib.stribog_hash.argtypes = [ctypes.c_char_p, ctypes.c_size_t, ctypes.c_char_p, ctypes.c_int]
lib.stribog_hash.restype = None


def stribog_hash(message: bytes, bit_size: int) -> str:
    if bit_size not in [256, 512]:
        raise ValueError("Поддерживаются только 256 или 512 бит.")

    hash_output = ctypes.create_string_buffer(bit_size // 8)
    lib.stribog_hash(message, len(message), hash_output, bit_size)
    return hash_output.raw.hex()


def start_stribog(message, size: int) -> str:
    if isinstance(message, str):
        message = message.encode('utf-8')
    return stribog_hash(message, size)


def count_bit_differences(hash1: str, hash2: str) -> int:
    """Подсчитывает количество различающихся битов между двумя хэшами."""
    bin1 = bin(int(hash1, 16))[2:].zfill(len(hash1) * 4)
    bin2 = bin(int(hash2, 16))[2:].zfill(len(hash2) * 4)
    return sum(b1 != b2 for b1, b2 in zip(bin1, bin2))


if __name__ == "__main__":
    messages = ["Привет", "Привер"]
    bit_sizes = [256, 512]

    for bit_size in bit_sizes:
        hashes = []
        for msg in messages:
            t = time.time()
            h = start_stribog(msg, bit_size)
            t_exec = time.time() - t
            hashes.append(h)
            print(f"Сообщение: {msg}")
            print(f"Длина выходной строки для {bit_size} бит: {bit_size}")
            print(f"Выходная строка для {bit_size} бит в hex: {h}")
            print(f"Время выполнения: {t_exec:.5f} сек\n")

        # Подсчет различий в битах
        bit_diff = count_bit_differences(hashes[0], hashes[1])
        print(f"Количество различающихся битов для {bit_size} бит: {bit_diff}")
        print(f"Ожидаемое количество (примерно): {bit_size // 2}\n")

    with open("GOST/picture_big.jpg", 'rb') as f:
        msg = f.read()
    t = time.time()
    bit_size = 256
    h = start_stribog(msg, bit_size)
    t_exec = time.time() - t
    print(f"Длина выходной строки для {bit_size} бит: {bit_size}")
    print(f"Выходная строка для {bit_size} бит в hex: {h}")
    print(f"Время выполнения: {t_exec:.5f} сек\n")

    t = time.time()
    bit_size = 512
    h = start_stribog(msg, bit_size)
    t_exec = time.time() - t
    print(f"Длина выходной строки для {bit_size} бит: {bit_size}")
    print(f"Выходная строка для {bit_size} бит в hex: {h}")
    print(f"Время выполнения: {t_exec:.5f} сек\n")
