# REFERENCE: https://hands-on.cloud/working-with-kms-in-python-using-boto3/#How-to-encrypt-files-using-KMS-and-Boto3-in-Python

import boto3
import base64
from cryptography.fernet import Fernet

client = boto3.client('kms')

response = client.generate_data_key(
    KeyId = 'ab447b7c-fc9a-40b0-a1eb-8956223ec0cd',
    KeySpec = 'AES_256'
)

print(response)

print("Cipher Text: ", response['CiphertextBlob'])
print("Plain Text Raw: ", response['Plaintext'])
print("Plain Text Base64 Encoded: ", base64.b64encode(response['Plaintext']))

data_key_encrypted = response['CiphertextBlob']
data_key_plaintext = base64.b64encode(response['Plaintext'])


filename = 'kms.txt'

# Read the entire file into memory
with open(filename, 'rb') as file:
    file_contents = file.read()

# Encrypt the file
f = Fernet(data_key_plaintext)
file_contents_encrypted = f.encrypt(file_contents)

# Write the encrypted data key and encrypted file contents together
with open(filename + '.encrypted', 'wb') as file_encrypted:
    file_encrypted.write(
        len(data_key_encrypted).to_bytes(4,
                                        byteorder='big'))
    file_encrypted.write(data_key_encrypted)
    file_encrypted.write(file_contents_encrypted)

ROOT_DIR = '.'
ROOT_S3_DIR = '23215183-cloudstorage' #Bucket Name

s3 = boto3.client("s3")
bucket_config = {'LocationConstraint': 'ap-southeast-2'}

s3.upload_file('./kms.txt.encrypted', ROOT_S3_DIR, 'kms.txt.encrypted',
                ExtraArgs = {"ServerSideEncryption": "aws:kms", "SSEKMSKeyId":"arn:aws:kms:ap-southeast-2:523265914192:key/ab447b7c-fc9a-40b0-a1eb-8956223ec0cd"})


s3_resource = boto3.resource('s3')
bucket = s3_resource.Bucket('23215183-cloudstorage')

bucket.download_file('kms.txt.encrypted', '/home/lab4/kms.txt.encrypted')

encrypted_downloaded_file = 'kms.txt.encrypted'

# Decrypt the encrypted data key
def decrypt_data_key(data_key_encrypted):
    response = client.decrypt(CiphertextBlob=data_key_encrypted)

    # Return plaintext base64-encoded binary data key
    return base64.b64encode((response['Plaintext']))

# Decrypt the encrypted file
def decrypt_file(filename):
    # Read the encrypted file into memory
    with open(filename, 'rb') as file_encrypted:
        file_contents_encrypted = file_encrypted.read()

    data_key_encrypted_len = int.from_bytes(file_contents_encrypted[:4],
                                            byteorder='big') \
                             + 4
    data_key_encrypted = file_contents_encrypted[
        4:data_key_encrypted_len]

    # Decrypt the data key before using it
    data_key_plaintext = decrypt_data_key(data_key_encrypted)

    # Decrypt the rest of the file
    f = Fernet(data_key_plaintext)
    file_contents_decrypted = f.decrypt(file_contents_encrypted[data_key_encrypted_len:])

    # Write the decrypted file contents
    with open(filename + '.decrypted' , 'wb') as file_decrypted:
        file_decrypted.write(file_contents_decrypted)

# Call the function
decrypt_file(encrypted_downloaded_file)





