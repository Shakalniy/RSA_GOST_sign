from RSA import universal_functions as uni
from RSA import convert_file
import time
import hashlib


main_folder = 'signed_files'


def get_open_key(file_name):
    return [int(x) for x in get_file_text(file_name).split("\n")]


def get_file_text(file_name):
    with open(file_name, 'r') as f:
        return f.read()


def check_sign(file_path):
    result = ""
    file_name = file_path.split('/')[-1].split('.')[0]
    folder_path = main_folder + "/" + "sign_" + file_name
    sign_file_name = folder_path + "/" + "sign_" + file_name + ".txt"
    open_key_name = folder_path + "/open_key_" + file_name + ".txt"

    if not uni.check_file_exists(sign_file_name) or not uni.check_file_exists(open_key_name):
        return "Подпись не найдена."

    t = time.time()

    e, n = get_open_key(open_key_name)

    bytes = convert_file.convert_file_to_bits(file_path, n)
    
    # хэширование
    hash = int.from_bytes(hashlib.sha256(bytes.encode()).digest())
    sign = uni.power(int(get_file_text(sign_file_name)), e, n)

    if sign == hash:
        result = "Подпись верная."
    else:
        result = "Подпись неверная."

    t = (time.time() - t).__round__(2)
    print(result)
    print("\nВремя работы программы:", t)

    return result
