from Crypto.PublicKey import RSA

def generate_keys_as_files():
    key = RSA.generate(2048)
    public = key.publickey().exportKey("PEM")
    private = key.exportKey("PEM")
    with open('public.pem', 'wb') as f:
        f.write(public)
        f.close()
    with open('private.pem', 'wb') as f:
        f.write(private)
        f.close()

def encrypt_with_file(fname, text):
    with open(fname, 'r') as f:
        key = RSA.importKey(f.read())
        return key.encrypt(text.encode(), 32)[0]

def decrypt_with_file(fname, text):
    with open(fname, 'r') as f:
        key = RSA.importKey(f.read())
        return key.decrypt(text)

ciphertext = encrypt_with_file("public.pem", "hello world")
solved = decrypt_with_file("private.pem", ciphertext)
print(solved.decode())
