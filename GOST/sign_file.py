from GOST.gen_params import gen_params
from GOST.gen_keys import gen_keys
from GOST.stribog import start_stribog
from random import randint
import sys
import os
import time
original_dir = os.getcwd()
sys.path.append(os.path.dirname(os.path.dirname(__file__)))
import universal_functions as uni
from sage.all import *
os.chdir(original_dir)


main_folder = 'signed_files/GOST'


def gen_sign(q, P, d, h):
    e = h % q
    if e == 0: e = 1
    r, k, C, s = 0, 0, 0, 0
    while r == 0 or s == 0:
        k = randint(1, q-1)
        C = k * P
        r = int(C[0]) % q
        s = (r * d + k * e) % q
    return r, s


def sign_file(file_path):
    file_name = file_path.split('/')[-1].split('.')[0]
    t = time.time()

    p, a, b, m, q, P = gen_params()
    l = 256
    d, Q = gen_keys(q, P)
    params = str(p) + "\n" + str(q) + "\n" + str(P) + "\n" + str(Q) + "\n" + str(a) + "\n" + str(b)
    
    folder_path = main_folder + "/" + "sign_" + file_name
    uni.create_folder(folder_path)
    uni.safe_file(folder_path + "/open_key_" + file_name + ".txt", params)

    M = open(file_path, 'r', encoding='utf-8').read()
    h = int(start_stribog(M, l), 16)
    r, s = gen_sign(q, P, d, h)
    r_bin = format(r, f'0{l}b')
    s_bin = format(s, f'0{l}b')
    zeta_bin = r_bin + s_bin

    uni.safe_file(folder_path + "/sign_" + file_name + ".txt", zeta_bin)

    t = (time.time() - t).__round__(2)
    print("\nProgram execution time:", t)