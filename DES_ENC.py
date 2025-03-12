
def text_to_binary(text):
    binary_result = ''.join(format(ord(char), '08b') for char in text)
    return binary_result
#====================================================================================
def int_to_binary(number):
    binary = bin(number)[2:]
    return binary.zfill(4)
#====================================================================================
def binary_to_decimal(binary_string):
    decimal_value = 0
    power = 0
    for digit in reversed(binary_string):
        if digit == '1':
            decimal_value += 2 ** power
        power += 1
    return decimal_value
#====================================================================================
def permutation(plaintext_in, ip):
    after_ip = ""
    for index in ip:
        after_ip += plaintext_in[index - 1]
    return after_ip
#====================================================================================
def r_expansion(plaintext_right, E):
    after_expansion = ""
    for index in E:
        after_expansion += plaintext_right[index - 1]
    return after_expansion
#====================================================================================
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

#====================================================================================

def sbox(plaintext_binary, S_BOXES):
    result = ""
    row_bits = ""
    column_bits = ""
    round = 0
    for i in range(8):
        row_bits = plaintext_binary[round] + plaintext_binary[round + 5]
        row = binary_to_decimal(row_bits)

        column_bits = plaintext_binary[round + 1 : round + 5]
        column = binary_to_decimal(column_bits)

        result += int_to_binary(S_BOXES[i][row][column])
        round += 6
    return result

#====================================================================================
def des_encrypt(binary, key, E, P, S_BOXES):

    binary_initial_permutation = binary
    #print("after initial permutation: " + binary_initial_permutation)
    half_point = len(binary_initial_permutation) // 2
    left_half = binary_initial_permutation[:half_point]
    #print("left half: " + left_half)
    right_half = binary_initial_permutation[half_point:]
    #print("right half: " + right_half)

    right_expanded = r_expansion(right_half, E)
    #print("right expanded: " + right_expanded)
    xored_right = xor(right_expanded, key)
    #print("xored right: " + xored_right)
    sbox_result = sbox(xored_right, S_BOXES)
    #print("sbox result: " + sbox_result)

    permutated_right = permutation(sbox_result , P)
    #print("permutated right: " + permutated_right)
    xored_left = xor(permutated_right , left_half)
    #print("xored left: " + xored_left)

    final_result = right_half + xored_left
    #print("final result: " + final_result)
    return final_result
#====================================================================================
