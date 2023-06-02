from database import connect
from psycopg2 import Error


def is_credenciales_correcta(correo, contraseña):
  resultado = False
  with connect.get_connection() as con:
    with con.cursor() as cursor:
      cursor = con.cursor()
      cursor.execute("SELECT EXISTS \
                    (SELECT 1 FROM usuario WHERE correo = %s AND contrasena = %s) \
                     AS existe_usuario;", (correo, contraseña));
    
      resultado = cursor.fetchone()[0]

  return resultado


def get_rol_usuario(correo):
  resultado = None
  with connect.get_connection() as con:
    with con.cursor() as cursor:
      cursor = con.cursor()
      cursor.execute("SELECT rol_id \
                      FROM usuario \
                      WHERE correo = %s;", (correo, ));
      resultado = cursor.fetchone()

  return resultado


def ingresar_miembro(correo, 
                     contraseña, 
                     nombre, 
                     edad, 
                     direccion, 
                     telefono, 
                     fecha_vencimiento, 
                     tipo_membresia):
  with connect.get_connection() as con:
    rowcount = 0
    with con.cursor() as cursor:
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
        rowcount = cursor.rowcount > 0
      except(Exception, Error) as error:
          print("Error: %s" % error)
          con.rollback()

    return rowcount > 0

def get_nombre_usuario(correo):
  pass