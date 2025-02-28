from stribog_constants import IV_512, IV_256, IV_512_HEX, IV_256_HEX, S_BOX, P_TABLE, L_MATRIX, C


def check_constants():
    print("512-bit IV (bytes):", IV_512)
    print("256-bit IV (bytes):", IV_256)

    # Output in hexadecimal format
    print("512-bit IV (hex):", IV_512_HEX)
    print("256-bit IV (hex):", IV_256_HEX)

    # Check array length
    print("Length of S_BOX:", len(S_BOX))

    # Output first 10 elements for verification
    print("First 10 elements of S_BOX:", S_BOX[:10])

    # Check array length
    print("Length of P:", len(P_TABLE))

    # Output first 10 elements for verification
    print("First 10 elements of P:", P_TABLE[:10])

    # Check matrix dimensions
    print("Matrix L dimensions:", len(L_MATRIX), "x", len(L_MATRIX[0]))

    # Output first two rows for verification
    print("First two rows of matrix L:")
    for row in L_MATRIX[:2]:
        print(row)
    
    # Check array C length
    print("Length of array C:", len(C))

    # Output first two elements for verification
    print("First two elements of array C:")
    for c in C[:2]:
        print(c)


if __name__ == "__main__":
    check_constants()
