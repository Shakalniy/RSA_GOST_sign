from stribog_constants import IV_512, IV_256, IV_512_HEX, IV_256_HEX, S_BOX, P_TABLE, L_MATRIX, C


def check_constants():
    print("512-bit IV (bytes):", IV_512)
    print("256-bit IV (bytes):", IV_256)

    # Вывод в шестнадцатеричном формате
    print("512-bit IV (hex):", IV_512_HEX)
    print("256-bit IV (hex):", IV_256_HEX)

    # Проверка длины массива
    print("Length of S_BOX:", len(S_BOX))

    # Вывод первых 10 элементов для проверки
    print("First 10 elements of S_BOX:", S_BOX[:10])

    # Проверка длины массива
    print("Length of P:", len(P_TABLE))

    # Вывод первых 10 элементов для проверки
    print("First 10 elements of P:", P_TABLE[:10])

    # Проверка размерности матрицы
    print("Matrix L dimensions:", len(L_MATRIX), "x", len(L_MATRIX[0]))

    # Вывод первых двух строк для проверки
    print("First two rows of matrix L:")
    for row in L_MATRIX[:2]:
        print(row)
    
    # Проверка длины массива C
    print("Length of array C:", len(C))

    # Вывод первых двух элементов для проверки
    print("First two elements of array C:")
    for c in C[:2]:
        print(c)


if __name__ == "__main__":
    check_constants()
