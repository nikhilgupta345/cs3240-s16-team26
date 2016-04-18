from Crypto.PublicKey import RSA
from Crypto.Cipher import AES
from Crypto import Random

def secret_string(string, public_key):
    encoded_string = public_key.encrypt(str.encode(string), 32)

    return encoded_string

def encrypt_file(file_name, symm_key):

    try:
        fout = open(file_name + '.enc', 'wb')

        text = ''
        with open(file_name, 'rb') as f:
            text = f.read()

        #print(text)

        enc = AES.new(symm_key, AES.MODE_CFB, b'abcdefghijklmnop')
        final_string = enc.encrypt(text)

        fout.write(final_string)

        fout.close()

        return True
    except IOError as ex:
        print("IO Error. File not valid.")
        return False
    except ValueError as ex:
        print(ex)
        print("Invalid key.")
        return False

def decrypt_file(file_name, symm_key):

    totaltext = ''
    try:
        with open(file_name, 'rb') as f:
            totaltext = f.read()

        dec = AES.new(symm_key, AES.MODE_CFB, b'abcdefghijklmnop')
        plaintext = dec.decrypt(totaltext)

        #print(plaintext)

        newfile = 'DEC_' + file_name[:-4]
        fout = open(newfile, 'wb')
        fout.write(plaintext)
        fout.close()
    except FileNotFoundError as ex:
        print(ex)
        print("File not found.")
    except UnicodeDecodeError as ex:
        print("Unicode Decode Error.")
    except ValueError as ex:
        print("Invalid Key Provided.")




if __name__ == '__main__':
    random_generator = Random.new().read
    key = RSA.generate(1024, random_generator)

    public = key.publickey()

    string = 'abcdefgh'
    secret = secret_string(string, public)

    #print(string)
    #print(secret)
    #print(key.decrypt(secret))

    filename = 'testpic.jpg'
    key = b'mysecretpassword'

    encrypt_file(filename, key)

    #print(len('\x03\x11M(h\xee\tM\x99\xb3\x03\x1dU\xec\xba\xe1'))

    decfile = 'testpic.jpg.enc'
    decrypt_file(decfile, key)