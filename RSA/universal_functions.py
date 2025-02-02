import os


def power(x, y, n):
    c = 1
    while y > 0:
        if y % 2 == 0:
            x = (x * x) % n
            y = y >> 1
        else:
            c = (c * x) % n
            y -= 1
    return c


def gcd(a, b):
    while a != 0 and b != 0:
        if a >= b:
            a %= b
        else:
            b %= a
    return a or b


def print_large_num(pred, n):
    s = str(n)
    l = len(s)
    print(pred, end="")
    for i in range(0, l, 100):
        if i + 100 < len(s):
            print(s[i: i + 100])
        else:
            print(s[i: l])
    return ""


def input_file_name(prompt, folder=""):
    while True:
        try:
            file_name = input(prompt)
            with open(folder + file_name, 'r') as f:
                return file_name
            break
        except FileNotFoundError:
            print("Файл не найден.")


def create_folder(file_name):
    try:
        folder_path = file_name.split('.')[0]
        os.makedirs(folder_path, exist_ok=True)
        print(f"Папка '{folder_path}' успешно создана.")
    except FileExistsError:
        print(f"Папка '{folder_path}' уже существует.")


def safe_file(file_name, n):
    with open(file_name, 'w') as f:
        f.write(n)
    print(f"Файл {file_name} сохранен.")
