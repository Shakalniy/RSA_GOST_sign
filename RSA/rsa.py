from RSA import sign_file, check_sign


def print_menu():
    print("\nЧто сделать?")

    print("1. Подписать файл")
    print("2. Проверить подпись файла")
    print("3. Выход")

    choice = input("Введите ваш выбор: ")

    return choice


def rsa_sign():
    while True:
        choice = print_menu()
        if choice == "1":
            sign_file.sign_file()
        elif choice == "2":
            check_sign.check_sign()
        elif choice == "3":
            break
        else:
            print("Неверный выбор. Пожалуйста, попробуйте еще раз.")
