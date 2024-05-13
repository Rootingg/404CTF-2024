import sympy
import binascii

# RSA parameters
p = 225147186137884341518974293808714674320589178485877061704235192167190874758244290619223094506656262149878982967706785355341806491582664373337816090887529
q = 267072171021243325740151821715997617064755331410341913960000482968308128907965160143499617129859867481580194055745752648594305889420259813632593867352463
e = 65537
c = 15129303695051503318505193172155921684909431243538868778377472653134183034984012506799855760917107279844275732327557949646134247015031503441468669978820652020054856908495646419146697920950182671202962511480958513703999302195279666734261744679837757391212026023983284529606062512100507387854428089714836938

# Calculate n and the totient φ(n)
n = p * q
phi_n = (p - 1) * (q - 1)

# Compute the decryption key d
d = sympy.mod_inverse(e, phi_n)

# Decrypt the ciphertext
m = pow(c, d, n)

# Convert the number to a hexadecimal string
hex_string = format(m, 'x')
if len(hex_string) % 2:  # Ensure length is even for proper conversion
    hex_string = '0' + hex_string

# Convert hexadecimal to bytes
byte_data = bytes.fromhex(hex_string)

# Convert bytes to ASCII text
ascii_text = byte_data.decode('ascii')

print("Decrypted ASCII Text:", ascii_text)
