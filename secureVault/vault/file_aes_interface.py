import ctypes
import os


BLOCK_SIZE = 32  


StateArray = (ctypes.c_ubyte * BLOCK_SIZE)


RoundKeysArray = (StateArray * 15)



lib_path = os.path.join(os.path.dirname(__file__), "aes.dll")
_AES_DLL = None

try:
    _AES_DLL = ctypes.CDLL(lib_path)
    
 
    _AES_DLL.encrypt.argtypes = [ctypes.POINTER(StateArray), ctypes.POINTER(RoundKeysArray)]
    _AES_DLL.encrypt.restype = ctypes.c_int

    _AES_DLL.decrypt.argtypes = [ctypes.POINTER(StateArray), ctypes.POINTER(RoundKeysArray)]
    _AES_DLL.decrypt.restype = ctypes.c_int
    
except Exception as e:
 
    print(f"ERROR: Failed to load AES DLL at {lib_path}. Encryption/Decryption will fail: {e}")
if _AES_DLL is None:
    print("⚠️ WARNING: aes.dll not loaded. Encryption disabled.")




_AES_DLL.set_key.argtypes = [ctypes.POINTER(ctypes.c_ubyte)]
_AES_DLL.set_key.restype = None

from hashlib import sha256

def set_cipher_key_from_password(password: str):
    """
    Derives a 32-byte key from user password and injects it into the DLL.
    """
    key = sha256(password.encode()).digest() 
    
    if len(key) != 32:
        raise ValueError("Key must be exactly 32 bytes") # 32 bytes
    _AES_DLL.set_key((ctypes.c_ubyte * 32)(*key))


ROUND_KEYS = RoundKeysArray() 

def _c_process_block(block: bytes, is_encrypt: bool) -> bytes:
    """Processes a single 32-byte block using the C library."""
    if len(block) != BLOCK_SIZE:
        raise ValueError("Block must be exactly 32 bytes.")

    state = StateArray.from_buffer_copy(block)
  
    if is_encrypt:
       
        result_code = _AES_DLL.encrypt(ctypes.byref(state), ctypes.byref(ROUND_KEYS))
    else:
        result_code = _AES_DLL.decrypt(ctypes.byref(state), ctypes.byref(ROUND_KEYS))
        
   
    if result_code != 0:
        raise RuntimeError(f"C AES operation failed with code {result_code}.")

    return bytes(state)


def aes_encrypt(data: bytes) -> bytes:
    """Encrypts raw bytes data using PKCS#7-like padding."""
    if not _AES_DLL:
        raise RuntimeError("AES DLL is not loaded. Cannot encrypt.")

    data_len = len(data)
    padding_len = BLOCK_SIZE - (data_len % BLOCK_SIZE)
  
    data_padded = data + bytes([padding_len] * padding_len)
    
    output_data = bytearray()

    for i in range(0, len(data_padded), BLOCK_SIZE):
        block = data_padded[i:i + BLOCK_SIZE]
        output_data.extend(_c_process_block(block, True))
        
    return bytes(output_data)

def aes_decrypt(data: bytes) -> bytes:
    """Decrypts raw bytes data and strips padding with integrity check."""
    if not _AES_DLL:
        raise RuntimeError("AES DLL is not loaded. Cannot decrypt.")
        
    if len(data) == 0 or len(data) % BLOCK_SIZE != 0:
        raise ValueError("Encrypted data is corrupted or empty.")

    decrypted_data = bytearray()
    
   
    for i in range(0, len(data), BLOCK_SIZE):
        block = data[i:i + BLOCK_SIZE]
        decrypted_data.extend(_c_process_block(block, False))
        
    
    padding_len = decrypted_data[-1]
    
    if padding_len == 0 or padding_len > BLOCK_SIZE:
         raise ValueError(f"Invalid padding length detected: {padding_len}. Possible key mismatch or data corruption.")

    padding_bytes = decrypted_data[-padding_len:]
    if any(b != padding_len for b in padding_bytes):
        raise ValueError("Padding integrity check failed. Data is likely corrupted or key is incorrect.")

    
    return bytes(decrypted_data[:-padding_len])