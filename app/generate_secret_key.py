from cryptography.fernet import Fernet

# Generate a Fernet key
SECRET_KEY = Fernet.generate_key()

# Print the generated key
print(SECRET_KEY)
