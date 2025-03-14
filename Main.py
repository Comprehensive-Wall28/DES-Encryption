
import os
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
def des_encrypt(binary, key, E, P, S_BOXES, final_swap_flag):
    binary_initial_permutation = binary

    half_point = len(binary_initial_permutation) // 2
    left_half = binary_initial_permutation[:half_point]
    print(" ")
    print("left half: " + left_half)
    right_half = binary_initial_permutation[half_point:]
    print(" ")
    print("right half: " + right_half)

    right_expanded = r_expansion(right_half, E)
    print(" ")
    print("right expanded: " + right_expanded)
    xored_right = xor(right_expanded, key)
    print(" ")
    print("xored right: " + xored_right)
    sbox_result = sbox(xored_right, S_BOXES)
    print(" ")
    print("sbox result: " + sbox_result)

    permutated_right = permutation(sbox_result , P)
    print(" ")
    print("permutated right: " + permutated_right)
    xored_left = xor(permutated_right , left_half)
    print(" ")
    print("xored left: " + xored_left)

    if final_swap_flag:
        final_result = xored_left + right_half
        return final_result
    final_result = right_half + xored_left
    print(" ")
    print("final result: " + final_result)
    print("END OF ROUND")
    return final_result
#====================================================================================

IP = [58, 50, 42, 34, 26, 18, 10, 2, 60, 52, 44, 36, 28, 20, 12, 4,
      62, 54, 46, 38, 30, 22, 14, 6, 64, 56, 48, 40, 32, 24, 16, 8,
      57, 49, 41, 33, 25, 17, 9, 1, 59, 51, 43, 35, 27, 19, 11, 3,
      61, 53, 45, 37, 29, 21, 13, 5, 63, 55, 47, 39, 31, 23, 15, 7]

E = [32, 1, 2, 3, 4, 5, 4, 5, 6, 7, 8, 9, 8, 9, 10, 11, 12, 13, 12, 13, 14, 15, 16, 17,
     16, 17, 18, 19, 20, 21, 20, 21, 22, 23, 24, 25, 24, 25, 26, 27, 28, 29, 28, 29, 30, 31, 32, 1]

S_BOXES = [
    [[14, 4, 13, 1, 2, 15, 11, 8, 3, 10, 6, 12, 5, 9, 0, 7],
     [0, 15, 7, 4, 14, 2, 13, 1, 10, 6, 12, 11, 9, 5, 3, 8],
     [4, 1, 14, 8, 13, 6, 2, 11, 15, 12, 9, 7, 3, 10, 5, 0],
     [15, 12, 8, 2, 4, 9, 1, 7, 5, 11, 3, 14, 10, 0, 6, 13]],

    [[15, 1, 8, 14, 6, 11, 3, 4, 9, 7, 2, 13, 12, 0, 5, 10],
     [3, 13, 4, 7, 15, 2, 8, 14, 12, 0, 1, 10, 6, 9, 11, 5],
     [0, 14, 7, 11, 10, 4, 13, 1, 5, 8, 12, 6, 9, 3, 2, 15],
     [13, 8, 10, 1, 3, 15, 4, 2, 11, 6, 7, 12, 0, 5, 14, 9]],

    [[10, 0, 9, 14, 6, 3, 15, 5, 1, 13, 12, 7, 11, 4, 2, 8],
     [13, 7, 0, 9, 3, 4, 6, 10, 2, 8, 5, 14, 12, 11, 15, 1],
     [13, 6, 4, 9, 8, 15, 3, 0, 11, 1, 2, 12, 5, 10, 14, 7],
     [1, 10, 13, 0, 6, 9, 8, 7, 4, 15, 14, 3, 11, 5, 2, 12]],

    [[7, 13, 14, 3, 0, 6, 9, 10, 1, 2, 8, 5, 11, 12, 4, 15],
     [13, 8, 11, 5, 6, 15, 0, 3, 4, 7, 2, 12, 1, 10, 14, 9],
     [10, 6, 9, 0, 12, 11, 7, 13, 15, 1, 3, 14, 5, 2, 8, 4],
     [3, 15, 0, 6, 10, 1, 13, 8, 9, 4, 5, 11, 12, 7, 2, 14]],

    [[2, 12, 4, 1, 7, 10, 11, 6, 8, 5, 3, 15, 13, 0, 14, 9],
     [14, 11, 2, 12, 4, 7, 13, 1, 5, 0, 15, 10, 3, 9, 8, 6],
     [4, 2, 1, 11, 10, 13, 7, 8, 15, 9, 12, 5, 6, 3, 0, 14],
     [11, 8, 12, 7, 1, 14, 2, 13, 6, 15, 0, 9, 10, 4, 5, 3]],

    [[12, 1, 10, 15, 9, 2, 6, 8, 0, 13, 3, 4, 14, 7, 5, 11],
     [10, 15, 4, 2, 7, 12, 9, 5, 6, 1, 13, 14, 0, 11, 3, 8],
     [9, 14, 15, 5, 2, 8, 12, 3, 7, 0, 4, 10, 1, 13, 11, 6],
     [4, 3, 2, 12, 9, 5, 15, 10, 11, 14, 1, 7, 6, 0, 8, 13]],

    [[4, 11, 2, 14, 15, 0, 8, 13, 3, 12, 9, 7, 5, 10, 6, 1],
     [13, 0, 11, 7, 4, 9, 1, 10, 14, 3, 5, 12, 2, 15, 8, 6],
     [1, 4, 11, 13, 12, 3, 7, 14, 10, 15, 6, 8, 0, 5, 9, 2],
     [6, 11, 13, 8, 1, 4, 10, 7, 9, 5, 0, 15, 14, 2, 3, 12]],

    [[13, 2, 8, 4, 6, 15, 11, 1, 10, 9, 3, 14, 5, 0, 12, 7],
     [1, 15, 13, 8, 10, 3, 7, 4, 12, 5, 6, 11, 0, 14, 9, 2],
     [7, 11, 4, 1, 9, 12, 14, 2, 0, 6, 10, 13, 15, 3, 5, 8],
     [2, 1, 14, 7, 4, 10, 8, 13, 15, 12, 9, 0, 3, 5, 6, 11]]
]
P = [16, 7, 20, 21, 29, 12, 28, 17, 1, 15, 23, 26, 5, 18, 31, 10,
     2, 8, 24, 14, 32, 27, 3, 9, 19, 13, 30, 6, 22, 11, 4, 25]

FP = [40, 8, 48, 16, 56, 24, 64, 32, 39, 7, 47, 15, 55, 23, 63, 31,
      38, 6, 46, 14, 54, 22, 62, 30, 37, 5, 45, 13, 53, 21, 61, 29,
      36, 4, 44, 12, 52, 20, 60, 28, 35, 3, 43, 11, 51, 19, 59, 27,
      34, 2, 42, 10, 50, 18, 58, 26, 33, 1, 41, 9, 49, 17, 57, 25]

key = "010101010101010101010101010101010101010101010101"

ROUNDS = 16

def pad_plaintext(binary_plaintext):
    padding_needed = 64 - (len(binary_plaintext) % 64)
    if padding_needed < 64:
        binary_plaintext += "1" + "0" * (padding_needed -1)
    else:
        binary_plaintext+= "1" + "0" * (padding_needed-1)
    return binary_plaintext

def split_into_blocks(binary_plaintext):
    blocks = [binary_plaintext[i:i + 64] for i in range(0, len(binary_plaintext), 64)]
    return blocks

def cbc_encrypt(plaintext, key, iv, E, P, S_BOXES):
    binary_plaintext = text_to_binary(plaintext)
    binary_plaintext = pad_plaintext(binary_plaintext)
    blocks = split_into_blocks(binary_plaintext)

    print("Binary_plaintext : " + binary_plaintext)

    ciphertext_blocks = []
    previous_block_cipher = iv
    for block_index, block in enumerate(blocks):
        print(f"\nEncrypting Block {block_index + 1}:")
        xored_block = xor(block, previous_block_cipher)
        print(f"  XORed with previous block cipher: {xored_block}")

        # Apply Initial Permutation
        current_binary = permutation(xored_block, IP)
        print(f"  After Initial Permutation: {current_binary}")
        print(" ")
        print("Inside DES round:")

        # DES Encryption Rounds
        final_swap_flag = False
        for i in range(ROUNDS):
            if i == 15:
                final_swap_flag = True
            current_binary = des_encrypt(current_binary, key, E, P, S_BOXES, final_swap_flag)
            if i == 15:
                current_binary = permutation(current_binary, FP)

            #print(f" Final result of round {i + 1}: {current_binary}")

        previous_block_cipher = current_binary
        ciphertext_blocks.append(current_binary)

    return "".join(ciphertext_blocks)

#========================================================================================================

plaintext = input("Plaintext: ")
mode = input("Mode (1 is stream, 2 is CBC: ")

if mode == "2":
    # Generate a random 64-bit IV (Initialization Vector)
    iv = bin(int(os.urandom(8).hex(), 16))[2:].zfill(64)

    print(f"Plaintext: {plaintext}")
    print(f"IV: {iv}")

    ciphertext = cbc_encrypt(plaintext, key, iv, E, P, S_BOXES)
    print(f"\nCiphertext: {ciphertext}")
    print(f"Ciphertext Length : {len(ciphertext)}")

if mode == "1":
    binary = text_to_binary(plaintext)
    print("binary: " + binary)

    current_binary = permutation(binary, IP)
    final_swap_flag = False

    for i in range(ROUNDS):
        if i == 15:
            final_swap_flag = True
        current_binary = des_encrypt(current_binary, key, E, P, S_BOXES, final_swap_flag)
        current_binary = permutation(current_binary, FP) #FINAL PERMUTATION
        print(f"Final result of round {i + 1}  :  {current_binary}")
        print("#======================================================================================#")
#========================================================================================================