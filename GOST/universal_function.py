def input_number(prompt):
    while True:
        try:
            num = int(input(prompt))
            return num
        except ValueError:
            print("Неверный ввод. Пожалуйста, введите число.")
            