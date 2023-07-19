from Cryptodome.Util.number import long_to_bytes,getStrongPrime, bytes_to_long,inverse
from pwn import *
import json
from Cryptodome.Cipher import AES
from Cryptodome.Util.Padding import pad, unpad
import hashlib
import binascii

context.log_level ='critical'

# Decryption function that reverses the given encryption
def decrypt_flag(shared_secret, iv, ciphertext):
    key = hashlib.sha1(str(shared_secret).encode()).hexdigest()[:16].encode()
    cipher = AES.new(key, AES.MODE_CBC, iv)
    ciphertext_bytes = binascii.unhexlify(ciphertext)
    decrypted_bytes = cipher.decrypt(ciphertext_bytes)
    plaintext = unpad(decrypted_bytes, 16).decode()
    return plaintext

chall = remote('159.89.13.180',5639)
# =======================================
#   Getting First Public Data from Alice
# =======================================
print(chall.recvuntil(b'Alice: '))
alice_json = json.loads(chall.recvuntil(b'}'))
print(alice_json)

#========================================
#   Forging our JSON with A's public
#   key as the base instead.
#   (A value will change the shared 
#   secret only, so irrelevant)
#========================================
hacker_json = alice_json 
hacker_json.update({'g':alice_json['A']})
hacker_json.update({'A':1})

#========================================
#   Some poor Bob useless part
#========================================
print(chall.recvuntil(b'Intercepted from Bob: '))

bob_alice_json = json.loads(chall.recvuntil(b'}'))
print(bob_alice_json)

# ========================================
#   Getting the encrypted Flag
# ========================================
print(chall.recvuntil(b'Intercepted from Alice: '))
flag_json = json.loads(chall.recvuntil(b'}'))

# ========================================
#   Sending modified payload to Bob
# ========================================
print(chall.recvuntil(b'Bob connects to you, send him some parameters:'))
chall.sendline(json.dumps(hacker_json))


# ========================================
#   Getting Shared Secret with Alice 
#   As Bob's shared secret
#   (small Brain Bob goes brrr!)
# ========================================
print(chall.recvuntil(b'Bob says to you: '))
bob_to_me = json.loads(chall.recvuntil(b'}'))
bob_secret = bob_to_me['B']
print(bob_to_me)

# ========================================
#   Decrypting Flag
# ========================================
iv = bytes.fromhex(flag_json['iv'])
ciphertext = flag_json['encrypted']

print(decrypt_flag(bob_secret, iv, ciphertext))

