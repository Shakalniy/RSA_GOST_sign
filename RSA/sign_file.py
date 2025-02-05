from RSA import gen_keys
from RSA import gen_prime_nums as prime
from RSA import universal_functions as uni
from RSA import convert_file
import time
import hashlib


size = 1024
main_folder = 'signed_files'


def sign_file():
    # конвертация текста
    file_name = uni.input_file_name("Введите имя подписываемого файла: ")
    t = time.time()

    # генерация p и q
    is_correct = False
    p, q, n = 0, 0, 0
    while not is_correct:
        p = prime.gen_secure_prime_num(size)
        q = prime.gen_secure_prime_num(size)
        if max(p, q) - min(p, q) > 2**(size/4):
            is_correct = True

    n = p * q
    print("Сгенерированные параметры:")
    print("p = ", p)
    print("q = ", q)
    print("n = ", n)

    # генерация ключей
    phi_n = (p - 1) * (q - 1)
    nod = uni.gcd(p-1, q-1)
    nok = phi_n // nod
    e, d = gen_keys.gen_keys(n, phi_n, nok)

    print("Сгенерированное ключи:")
    print("e = ", e)
    print("d = ", d)
    
    folder_path = main_folder + "/" + "sign_" + file_name.split('.')[0]
    uni.create_folder(folder_path)
    uni.safe_file(folder_path + "/open_key_" + file_name.split('.')[0] + ".txt", str(e) + "\n" + str(n))

    bytes = convert_file.convert_file_to_bits(file_name, n)
    # хэширование
    hash = int.from_bytes(hashlib.sha256(bytes.encode()).digest())

    # подпись
    sign = uni.power(hash, d, n)
    uni.safe_file(folder_path + "/sign_" + file_name.split('.')[0] + ".txt", str(sign))

    t = (time.time() - t).__round__(2)
    print("\nВремя работы программы:", t)
