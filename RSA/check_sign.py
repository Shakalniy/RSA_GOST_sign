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


def check_sign():
    file_name = uni.input_file_name("Введите имя подписываемого файла: ")
    folder_path = main_folder + "/" + "sign_" + file_name.split('.')[0]
    sign_file_name = folder_path + "/" + uni.input_file_name("Введите имя файла с подписью: ", folder_path + "/")
    open_key_name = folder_path + "/open_key_" + file_name.split('.')[0] + ".txt"
    t = time.time()

    e, n = get_open_key(open_key_name)

    bytes = convert_file.convert_file_to_bits(file_name, n)
    
    # хэширование
    hash = int.from_bytes(hashlib.sha256(bytes.encode()).digest())
    sign = uni.power(int(get_file_text(sign_file_name)), e, n)

    if sign == hash:
        print("\nПодпись верная.")
    else:
        print("\nПодпись неверная.")

    t = (time.time() - t).__round__(2)
    print("\nВремя работы программы:", t)
