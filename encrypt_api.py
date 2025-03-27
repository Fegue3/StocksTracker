from cryptography.fernet import Fernet

# Gera a chave secreta
key = Fernet.generate_key()
with open("secret.key", "wb") as key_file:
    key_file.write(key)

# Define a tua API Key aqui
api_key = "6URUWRBGBU1BSUBU"

# Encripta a API Key
fernet = Fernet(key)
encrypted_api = fernet.encrypt(api_key.encode())

# Guarda a API encriptada num ficheiro
with open("api.enc", "wb") as f:
    f.write(encrypted_api)

print("✅ API Key encriptada e guardada com sucesso!")
