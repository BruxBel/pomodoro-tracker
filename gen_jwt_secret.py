import secrets

# Генерация безопасного ключа (64 символа, hex)
jwt_secret_key = secrets.token_hex(32)  # 64 символа (256 бит)
print(f"JWT_SECRET_KEY={jwt_secret_key}")
