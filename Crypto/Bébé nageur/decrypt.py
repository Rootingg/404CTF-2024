import sympy as sp

# Character set and its length
charset = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789{}_-!"
n = len(charset)

# Encryption function
def f(a, b, n, x):
    return (a * x + b) % n

def encrypt(message, a, b, n):
    encrypted = ""
    for char in message:
        x = charset.index(char)
        x = f(a, b, n, x)
        encrypted += charset[x]
    return encrypted

# Decryption function
def decrypt(encrypted, a_inv, b, n):
    decrypted = ""
    for char in encrypted:
        y = charset.index(char)
        x = (a_inv * (y - b)) % n
        decrypted += charset[x]
    return decrypted

# Function to find the parameters a and b
def find_parameters(known, encrypted):
    for a in range(2, n):
        for b in range(1, n):
            if encrypt(known, a, b, n) == encrypted:
                return a, b
    return None, None

# Example usage: Decrypting a given encrypted flag
known_start = "404CTF{"
encrypted_start = "-4-c57T"
a_found, b_found = find_parameters(known_start, encrypted_start)

if a_found and b_found:
    a_inv = sp.mod_inverse(a_found, n)
    encrypted_flag = "-4-c57T5fUq9UdO0lOqiMqS4Hy0lqM4ekq-0vqwiNoqzUq5O9tyYoUq2_"
    decrypted_flag = decrypt(encrypted_flag, a_inv, b_found, n)
    print("Decrypted Flag:", decrypted_flag)
else:
    print("Failed to find valid parameters.")
