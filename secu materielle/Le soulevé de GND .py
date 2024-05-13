A = 7
B = 1918273
N = 25
data = [
    78, 114, 87, 9, 245, 67, 252, 90, 90, 126, 120, 109, 133, 78, 206, 121, 52, 115,
    123, 102, 164, 194, 170, 123, 5
]

# Calculate the initial sequence of states based on the GND function
states = [0] * N  # Initialize states array
for i in range(1, N):
    states[i] = (A * states[i-1] + B) % 256

# Reverse-engineer the input values that would generate the correct outputs
input_values = [0] * N
for i in range(N):
    input_values[i] = states[i] ^ data[i]

# Convert numeric input values to characters assuming they are ASCII
input_chars = [chr(v) if 0 <= v < 256 else '?' for v in input_values]
input_string = ''.join(input_chars)

print(f"Generated input string: {input_string}")
if len(input_string) == N:
    print(f"Flag: 404CTF{{{input_string}}}")
else:
    print("Failed to generate a valid input string of required length.")

# Flag: 404CTF{N3_perd3z_P45_v0tr3_t3rRe}