from pwn import *
import angr
import sys
import claripy
import os

def fetch_binary():
    os.system('nc challenges.404ctf.fr 31998 > chall.zip')

def decompress_binary():
    os.system('unzip chall.zip')

def get_token_value():
    with open('token.txt', 'r') as f:
        token_value = f.read().strip()
    print("Token:", token_value)
    return token_value

def send_value(value1, value2):
    conn = remote('challenges.404ctf.fr', 31999)
    conn.sendline(value1)
    conn.sendline(value2)
    response = conn.recv()
    flag = conn.recv()
    print(response)
    print(flag)

def is_successful(state):
    output = state.posix.dumps(sys.stdout.fileno())
    if b'GG' in output:
        return True
    return False

def solve(elf_binary="./crackme.bin"):
    project = angr.Project(elf_binary)
    argv = claripy.BVS('argv', 8 * 16)
    initial_state = project.factory.entry_state(args=[elf_binary, argv])
    simulation = project.factory.simgr(initial_state)
    simulation.explore(find=is_successful)
    if simulation.found:
        for solution_state in simulation.found:
            password = solution_state.solver.eval(argv, cast_to=bytes)
            print("[>>] Password found: {!r}".format(password))
            return password
    else:
        print("[>>] No solution found :(")
        return None

def main():
    fetch_binary()
    decompress_binary()
    password = solve()
    token_value = get_token_value()
    if password:
        send_value(token_value, password)

if __name__ == "__main__":
    main()
