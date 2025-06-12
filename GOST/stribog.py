import ctypes
import os
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
