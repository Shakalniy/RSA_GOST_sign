import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(__file__)))
from RSA.gen_params import gen_params
from RSA.sha256 import sha256
import universal_functions as uni
import time


size = 1024
main_folder = 'signed_files/RSA'


def sign_file(file_path, constants=None):
    file_name = file_path.split('/')[-1].split('.')[0]
    bytes = open(file_path, 'rb').read()
    
    # Проверка на пустой файл
    if len(bytes) == 0:
        raise ValueError("Ошибка: файл пустой.")

    t = time.time()

    if constants:
        n = constants.n
        e = constants.e
        d = constants.d
    else:
        n, e, d = gen_params()

    # print("Generated keys:")
    # print("e = ", e)
    # print("d = ", d)
    
    folder_path = main_folder + "/" + "sign_" + file_name
    uni.create_folder(folder_path)
    uni.safe_file(folder_path + "/open_key_" + file_name + ".txt", str(e) + "\n" + str(n))

    t1 = time.time()
    
    hash = int.from_bytes(sha256(bytes), byteorder='big')
    t2 = time.time()
    print("Время выполнения SHA256:", t2 - t1)

    sign = uni.power(hash, d, n)
    uni.safe_file(folder_path + "/sign_" + file_name + ".txt", str(sign))

    t3 = time.time()
    t = (time.time() - t)
    print("Время создания подписи:", t3 - t2)
    print("Общее время выполнения программы:", t)
    return folder_path.split('/')[-1]


if __name__ == '__main__':
    from memory_profiler import profile
    @profile
    def start_sign():
        sign_file("README.md")
        pass
    
    start_sign()
