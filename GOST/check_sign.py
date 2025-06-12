import sys
import os
import time
original_dir = os.getcwd()
sys.path.append(os.path.dirname(os.path.dirname(__file__)))
import universal_functions as uni
from GOST.stribog import start_stribog
from sage.all import *
os.chdir(original_dir)


main_folder = 'signed_files/GOST'


def string_to_point(point_str, p, a, b):
    coords = point_str.strip("()").replace(" ", "").split(":")
    if len(coords) != 3:
        raise ValueError("Строка должна содержать 3 координаты: (x : y : z).")
        
    x = int(coords[0])
    y = int(coords[1])
    z = int(coords[2])
        
    if z != 1:
        raise ValueError("Поддерживаются только аффинные координаты (z = 1).")
        
    F = GF(p)
    try:
        E = EllipticCurve(F, [a, b])
    except ValueError:
        raise ValueError("Недействительные параметры кривой: 4a^3 + 27b^2 ≡ 0 mod p.")
        
    try:
        P = E(x, y)
    except ValueError:
        raise ValueError(f"Точка ({x}, {y}) не лежит на кривой E: y^2 = x^3 + {a}x + {b} mod {p}")
        
    return P


def get_params(file_name):
    p, q, P, Q, a, b = [x for x in get_file_text(file_name).split("\n")]
    P_point = string_to_point(P, int(p), int(a), int(b))
    Q_point = string_to_point(Q, int(p), int(a), int(b))
    return int(q), P_point, Q_point


def get_file_text(file_name):
    with open(file_name, 'r') as f:
        return f.read()


def check_sign(file_path, l = 256):
    try:
        file_name = file_path.split('/')[-1].split('.')[0]
        folder_path = main_folder + "/" + "sign_" + file_name
        sign_file_name = folder_path + "/" + "sign_" + file_name + ".txt"
        open_key_name = folder_path + "/open_key_" + file_name + ".txt"

        if not uni.check_file_exists(sign_file_name) or not uni.check_file_exists(open_key_name):
            return "Подпись не найдена"
        
        t = time.time()

        zeta_bin = get_file_text(sign_file_name)
        M = open(file_path, 'rb').read()
        q, P, Q = get_params(open_key_name)

        r = int(zeta_bin[:l], 2)
        s = int(zeta_bin[l:], 2)

        if r > q or s > q: return "Подпись не действительна"

        t1 = time.time()
        h = int(start_stribog(M, l), 16)
        t2 = time.time()
        print("Время выполнения Стрибог:", t2 - t1)

        e = h % q
        if e == 0: e = 1
        v = inverse_mod(e, q)

        z1 = s * v % q
        z2 = (q - r) * v % q
        C = z1 * P + z2 * Q
        R = int(C[0]) % q
    
        if R == r:
            result = "Подпись действительна"
        else:
            result = "Подпись не действительна"

        t3 = time.time()
        t = (time.time() - t)
        print("Время создания подписи:", t3 - t2)
        print("Общее время выполнения программы:", t)
        print(result)

        return result
    except Exception as e:
        print(e)
        return "Подпись не действительна"
