from database import connect
from psycopg2 import Error


def is_credenciales_correcta(correo, contraseña):
  with connect.get_connection() as con:
    cursor = con.cursor()
    cursor.execute("SELECT EXISTS \
                   (SELECT 1 FROM usuario WHERE correo = %s AND contrasena = %s) \
                   AS existe_usuario;", (correo, contraseña));
    return cursor.fetchone()[0]


def is_admin(correo):
  with connect.get_connection() as con:
    cursor = con.cursor()
    cursor.execute("SELECT EXISTS \
                   (SELECT 1 FROM administrador WHERE correo_administrador = %s) \
                   AS is_admin;", (correo, ));
    return cursor.fetchone()[0]


def ingresar_miembro(correo, 
                     contraseña, 
                     nombre, 
                     edad, 
                     direccion, 
                     telefono, 
                     fecha_vencimiento, 
                     tipo_membresia):
  with connect.get_connection() as con:
    cursor = con.cursor()
    try:
      con.autocommit = False
      cursor.execute("INSERT INTO usuario (correo, contrasena) VALUES (%s, %s);", (correo, contraseña))
      cursor.execute("INSERT INTO miembro \
                      (correo_miembro, \
                      nombre, \
                      edad, \
                      direccion, \
                      telefono, \
                      fecha_vencimiento, \
                      tipo_membresia) VALUES \
                      (%s, %s, %s, %s, %s, %s, %s)", (correo, 
                                                      nombre, 
                                                      edad, 
                                                      direccion, 
                                                      telefono, 
                                                      fecha_vencimiento, 
                                                      tipo_membresia))
      con.commit()
      print("cursor rowcount", cursor.rowcount)
      return cursor.rowcount > 0
    
    except(Exception, Error) as error:
        print("Error: %s" % error)
        con.rollback()
        return False

def get_nombre_usuario(correo):
  pass