from .file_aes_interface import (
    set_cipher_key_from_password,
    aes_encrypt,
    aes_decrypt
)

def encrypt_file_upload(file_obj, user_password: str) -> bytes:
    """
    Encrypts uploaded file using user password.
    """
    raw_bytes = file_obj.read()
    set_cipher_key_from_password(user_password)
    return aes_encrypt(raw_bytes)


def decrypt_file_download(encrypted_bytes: bytes, user_password: str) -> bytes:
    """
    Decrypts encrypted file using user password.
    """
    set_cipher_key_from_password(user_password)
    return aes_decrypt(encrypted_bytes)
