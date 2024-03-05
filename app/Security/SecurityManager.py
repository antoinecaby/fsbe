# security/SecurityManager.py
from passlib.context import CryptContext
from cryptography.fernet import Fernet

class SecurityManager:
    def __init__(self):
        self.pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
        self.key = Fernet.generate_key()
        self.fernet = Fernet(self.key)

    def verify_password(self, plain_password, hashed_password):
        return self.pwd_context.verify(plain_password, hashed_password)

    def get_password_hash(self, password):
        return self.pwd_context.hash(password)

    def encrypt(self, data):
        return self.fernet.encrypt(data.encode()).decode()

    def decrypt(self, encrypted_data):
        return self.fernet.decrypt(encrypted_data.encode()).decode()