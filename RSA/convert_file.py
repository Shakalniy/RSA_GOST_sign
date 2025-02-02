def open_file(file):
    with open(file, 'rb') as f:
        file_code = f.read()  # чтение файла по байтово

    return file_code


def write_file(file_code, file_name, sub):
    with open(f"{sub}_{file_name}", 'wb') as f:
        f.write(bytes(file_code))


def convert(file_code):
    bytes = ""
    for l in file_code:
        bytes += format(l, "08b")
    return bytes


def convert_to_bytes(bits):
    l = len(bits)
    bytes = []
    for i in range(0, l, 8):
        if i + 8 <= l:
            num = int(bits[i: i + 8], 2)
        else:
            num = int(bits[i: l], 2)
        bytes.append(num)

    return bytes


def convert_file_to_bits(file_name, n):
    bites = open_file(file_name)
    bites = convert(bites)
    return bites
