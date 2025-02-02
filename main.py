import RSA.rsa as rsa
import GOST.gost as gost

def print_menu():
    print("\nКакой метод использовать?")

    print("1. Цифровая подпись RSA")
    print("2. Цифровая подпись ГОСТ")
    print("3. Выход")

    choice = input("Введите ваш выбор: ")

    return choice


def main():
    while True:
        choice = print_menu()
        if choice == "1":
            rsa.rsa_sign()
        elif choice == "2":
            gost.gost()
        elif choice == "3":
            exit()
        else:
            print("Неверный выбор. Пожалуйста, попробуйте еще раз.")


if __name__ == '__main__':
    main()
