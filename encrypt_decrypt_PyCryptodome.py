import os, random, struct
from Crypto.Cipher import AES
from Crypto import Random
import boto3
import base64
import hashlib


BLOCK_SIZE = 16
CHUNK_SIZE = 64 * 1024

def encrypt_file(password, in_filename, out_filename):

    key = hashlib.sha256(password.encode("utf-8")).digest()

    iv = Random.new().read(AES.block_size)
    encryptor = AES.new(key, AES.MODE_CBC, iv)
    filesize = os.path.getsize(in_filename)

    with open(in_filename, 'rb') as infile:
        with open(out_filename, 'wb') as outfile:
            outfile.write(struct.pack('<Q', filesize))
            outfile.write(iv)

            while True:
                chunk = infile.read(CHUNK_SIZE)
                if len(chunk) == 0:
                    break
                elif len(chunk) % 16 != 0:
                    chunk += ' '.encode("utf-8") * (16 - len(chunk) % 16)

                outfile.write(encryptor.encrypt(chunk))


def decrypt_file(password, in_filename, out_filename):

    key = hashlib.sha256(password.encode("utf-8")).digest()

    with open(in_filename, 'rb') as infile:
        origsize = struct.unpack('<Q', infile.read(struct.calcsize('Q')))[0]
        iv = infile.read(16)
        decryptor = AES.new(key, AES.MODE_CBC, iv)

        with open(out_filename, 'wb') as outfile:
            while True:
                chunk = infile.read(CHUNK_SIZE)
                if len(chunk) == 0:
                    break
                outfile.write(decryptor.decrypt(chunk))

            outfile.truncate(origsize)


password = 'kitty and the kat'

encrypt_file(password,"kms_crpt.txt", out_filename="kms_crpt.txt.encrypted")

ROOT_DIR = '.'
ROOT_S3_DIR = '23215183-cloudstorage' #Bucket Name

s3 = boto3.client("s3")
bucket_config = {'LocationConstraint': 'ap-southeast-2'}

s3.upload_file('./kms_crpt.txt.encrypted', ROOT_S3_DIR, 'kms_crpt.txt.encrypted')

# Download the uploaded encrypted file
s3_resource = boto3.resource('s3')
bucket = s3_resource.Bucket('23215183-cloudstorage')

bucket.download_file('kms_crpt.txt.encrypted', '/home/lab4/kms_crpt.txt.encrypted')

encrypted_downloaded_file = 'kms_crpt.txt.encrypted'

# Decrypt the downloaded file
decrypt_file(password, "kms_crpt.txt.encrypted", out_filename="kms_crpt.txt.encrypted.decrypted")

