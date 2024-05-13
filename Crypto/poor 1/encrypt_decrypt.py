from my_random import Generator
from Cryptodome.Util.number import long_to_bytes
def xor(b1, b2):
    return bytes(a ^ b for a, b in zip(b1, b2))

def get_blocks(data,block_size):
	return [data[i:i+block_size] for i in range(0,len(data),block_size)]

def pad(data,block_size):
	return data+b'\x00'*(block_size-len(data)%block_size)

def encrypt(data,block_size):
	padded_data = pad(data,block_size)
	data_blocks = get_blocks(padded_data,block_size)
	generator = Generator()
	encrypted = b''

	for block in data_blocks:

		rd = generator.get_random_bytes(block_size)
		xored = xor(block,rd)
		encrypted+= xored
	return encrypted

BLOCK_SIZE = 4
flag = None




if __name__ == '__main__':
    cipher = "flag.png.enc"
    knowndata = "flag.png.part"
    with open(cipher,'rb') as f:
        cipher = f.read()
    with open(knowndata,'rb') as f:
        knowndata = f.read()

    knownbytes = [i for i in xor(knowndata,cipher[:len(knowndata)])]

    #we will create a generator using the feed that we think was used to generate the cipher
    generator = Generator()
    generator.feed = knownbytes[:2000]

    #we will test if we"re able to predict the next bytes
    #we will cipher the rest of the known data using the generator and compare it to the real cipher
    #if the ciphered block we created is the same as the real ciphered block, we can assume that we have the right feed
    trainingbytes = knowndata[2000:]
    tocompare = cipher[2000:len(knowndata)]
    for i in range(0,len(trainingbytes),BLOCK_SIZE):
        rd = generator.get_random_bytes(BLOCK_SIZE)
        xored = xor(trainingbytes[i:i+BLOCK_SIZE],rd)
        if xored != tocompare[i:i+BLOCK_SIZE]:
            print("Wrong feed")
            break
    
    #now that we're sure that we have the right feed, we can decrypt the rest of the cipher
    #by xoring the cipher with the get_random_bytes of the generator we created
    generator.feed = knownbytes[:2000]
    decrypted = b''
    for i in range(2000,len(cipher),BLOCK_SIZE):
        rd = generator.get_random_bytes(BLOCK_SIZE)
        xored = xor(cipher[i:i+BLOCK_SIZE],rd)
        decrypted+= xored

 
    with open("flag.png",'w+b') as f:
        f.write(knowndata[:2000]+decrypted)