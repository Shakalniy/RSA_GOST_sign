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
            print("Файл не найден.")


def create_folder(file_name):
    try:
        folder_path = file_name.split('.')[0]
        os.makedirs(folder_path, exist_ok=True)
        print(f"Папка '{folder_path}' успешно создана.")
    except FileExistsError:
        pass
        print(f"Папка '{folder_path}' уже существует.")


def safe_file(file_name, n):
    with open(file_name, 'w') as f:
        f.write(n)
    print(f"Файл {file_name} сохранен.")


def check_file_exists(file_path):
    try:
        with open(file_path, 'r') as f:
            return True
    except FileNotFoundError:
        return False


def gcd_extended(num1, num2):
    if num1 == 0:
        return num2, 0, 1
    else:
        div, x, y = gcd_extended(num2 % num1, num1)
    return div, y - (num2 // num1) * x, x

    
def input_number(prompt):
    while True:
        try:
            num = int(input(prompt))
            return num
        except ValueError:
            print("Неправильный ввод. Пожалуйста введите целое число.")