IP = [58, 50, 42, 34, 26, 18, 10, 2, 60, 52, 44, 36, 28, 20, 12, 4,
      62, 54, 46, 38, 30, 22, 14, 6, 64, 56, 48, 40, 32, 24, 16, 8,
      57, 49, 41, 33, 25, 17, 9, 1, 59, 51, 43, 35, 27, 19, 11, 3,
      61, 53, 45, 37, 29, 21, 13, 5, 63, 55, 47, 39, 31, 23, 15, 7]

E = [32, 1, 2, 3, 4, 5, 4, 5, 6, 7, 8, 9, 8, 9, 10, 11, 12, 13, 12, 13, 14, 15, 16, 17,
     16, 17, 18, 19, 20, 21, 20, 21, 22, 23, 24, 25, 24, 25, 26, 27, 28, 29, 28, 29, 30, 31, 32, 1]

key = "010101010101010101010101010101010101010101010101"  # Corrected key

plaintext = "Hello world!"

def text_to_binary(text):
    binary_result = ''.join(format(ord(char), '08b') for char in text)
    return binary_result

def permutation(plaintext_in, ip):
    plaintext_binary = text_to_binary(plaintext_in)
    after_ip = ""
    for index in ip:
        after_ip += plaintext_binary[index - 1]
    return after_ip

def r_expansion(plaintext_right):
    after_expansion = ""
    for index in E:
        after_expansion += plaintext_right[index - 1]
    return after_expansion

def xor(plaintext_in, key):
    xored_string = ""
    for i in range(len(plaintext_in)):  # Use len(plaintext_in) for flexibility
        if plaintext_in[i] == '0' and key[i] == '0':
            xored_string += "0"
        elif (plaintext_in[i] == '0' and key[i] == '1') or \
                (plaintext_in[i] == '1' and key[i] == '0'):
            xored_string += "1"
        elif plaintext_in[i] == '1' and key[i] == '1':
            xored_string += "0"
    return xored_string


def des_encrypt(plaintext_in, IP, key):
    permutated_plaintext_in = permutation(plaintext_in, IP)

    half_point = len(permutated_plaintext_in) // 2
    first_half = permutated_plaintext_in[:half_point]
    second_half = permutated_plaintext_in[half_point:]

    right_expanded = r_expansion(second_half) # Corrected to use second_half
    print(xor(right_expanded, key))  # Pass key to xor


des_encrypt(plaintext, IP, key)  # Pass key to des_encrypt