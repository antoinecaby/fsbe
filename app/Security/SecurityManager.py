# Security/SecurityManager.py
from typing import Union
from passlib.context import CryptContext
from cryptography.fernet import Fernet

class SecurityManager:
    def __init__(self, secret_key: bytes):
        self.pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
        self.key = secret_key
        self.fernet = Fernet(self.key)

    def verify_password(self, plain_password: str, hashed_password: str) -> bool:
        return self.pwd_context.verify(plain_password, hashed_password)

    def get_password_hash(self, password: str) -> str:
        return self.pwd_context.hash(password)

    def encrypt(self, data: str) -> str:
        return self.fernet.encrypt(data.encode()).decode()

    def decrypt(self, encrypted_data: Union[str, bytes]) -> str:
        # Ensure that encrypted_data is a string, then convert it to bytes
        if isinstance(encrypted_data, str):
            encrypted_data_bytes = encrypted_data.encode()
        else:
            encrypted_data_bytes = encrypted_data
        
        # Decode the base64 encoded bytes before decrypting
        decrypted_data = self.fernet.decrypt(encrypted_data_bytes)
        
        # Convert the decrypted result to string before returning
        return decrypted_data.decode()
