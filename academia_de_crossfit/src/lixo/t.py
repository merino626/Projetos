import bcrypt
from random import choice
import string


senha = ''
for i in range(8):
    senha += choice(string.ascii_lowercase + string.digits)


senha_hasheada = bcrypt.hashpw(senha.encode("utf-8"), bcrypt.gensalt())

print("senha",senha)
print("senha_hasheada",senha_hasheada)


if bcrypt.checkpw(senha.encode("utf-8"), senha_hasheada):
    print("logged")
else:
    print("Error :(")