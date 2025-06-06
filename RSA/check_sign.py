import universal_functions as uni
from RSA.sha256 import sha256
import time


main_folder = 'signed_files/RSA'


def get_open_key(file_name):
    return [int(x) for x in get_file_text(file_name).split("\n")]


def get_file_text(file_name):
    with open(file_name, 'r') as f:
        return f.read()


def check_sign(file_path):
    file_name = file_path.split('/')[-1].split('.')[0]
    folder_path = main_folder + "/" + "sign_" + file_name
    sign_file_name = folder_path + "/" + "sign_" + file_name + ".txt"
    open_key_name = folder_path + "/open_key_" + file_name + ".txt"
    if not uni.check_file_exists(sign_file_name) or not uni.check_file_exists(open_key_name):
        return "Signature not found."
    t = time.time()
    e, n = get_open_key(open_key_name)
    t1 = time.time()
    bytes = open(file_path, 'rb').read()
    hash = int.from_bytes(sha256(bytes), byteorder='big')
    t2 = time.time()
    print("Время выполнения SHA256:", t2 - t1)
    sign = uni.power(int(get_file_text(sign_file_name)), e, n)
    if sign == hash:
        result = "Signature is valid."
    else:
        result = "Signature is invalid."

    t3 = time.time()
    t = (time.time() - t)
    print("Время создания подписи:", t3 - t2)
    print("Общее время выполнения программы:", t)
    print(result)

    return result
