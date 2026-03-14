import bcrypt
print(bcrypt.hashpw(b'placeholder', bcrypt.gensalt()).decode())