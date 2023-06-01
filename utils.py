import random
import string
import re

def generar_contrasena():
    while True:
        contrasena = ''.join(random.choices(string.ascii_letters + string.digits, k=random.randint(6, 8)))
        if re.match('^(?=.*[A-Z])(?=.*\d).{6,8}$', contrasena):
            return contrasena