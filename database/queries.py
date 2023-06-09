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

  if resultado is None:
    resultado = []

  return resultado

def ingresar_miembro(correo, 
                     contraseña, 
                     nombre, 
                     edad, 
                     direccion, 
                     telefono, 
                     fecha_vencimiento, 
                     tipo_membresia):
  rowcount = 0
  with connect.get_connection() as con:
    with con.cursor() as cursor:
      cursor = con.cursor()
      try:
        con.autocommit = False
        cursor.execute("INSERT INTO usuario \
                       (correo, \
                       contrasena, \
                       rol_id) VALUES (%s, %s, %s);", (correo, contraseña, 2))
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
          print("\nError: %s\n" % error)
          con.rollback()

  return rowcount > 0

def get_datos_miembro(correo_miembro):
  resultado = None
  with connect.get_connection() as con:
    with con.cursor() as cursor:
      cursor = con.cursor()
      cursor.execute("SELECT nombre, \
                      edad, \
                      direccion, \
                      telefono, \
                      fecha_vencimiento, \
                      tipo_membresia \
                      FROM miembro \
                      WHERE correo_miembro = %s;", (correo_miembro, ));
      resultado = cursor.fetchone()

  if resultado is None:
    resultado = []

  return resultado

def actualizar_membresia(correo_miembro,
                        nueva_fecha_vencimiento,
                        nueva_membresia):
  actualizado = False
  with connect.get_connection() as con:
    with con.cursor() as cursor:
      cursor = con.cursor()
      try:
        con.autocommit = False
        cursor.execute("UPDATE miembro SET \
                       fecha_vencimiento=%s, \
                       tipo_membresia=%s \
                       WHERE correo_miembro=%s", (nueva_fecha_vencimiento,
                                                  nueva_membresia,
                                                  correo_miembro));
        con.commit()
        actualizado = True
      except(Exception, Error) as error:
          print("\nError: %s\n" % error)
          con.rollback()

  return actualizado

def get_datos_miembros_membresia_venc():
    resultado = None
    with connect.get_connection() as con:
      with con.cursor() as cursor:
        cursor = con.cursor()
        cursor.execute("SELECT nombre, \
                        edad, \
                        direccion, \
                        telefono, \
                        fecha_vencimiento, \
                        tipo_membresia \
                        FROM miembro \
                        WHERE fecha_vencimiento <= CURRENT_DATE;");
        resultado = cursor.fetchall()

    if resultado is None:
      resultado = []

    return resultado

def agregar_clase(
    id_clase, 
    nombre_instructor, 
    horario):
  rowcount = 0
  with connect.get_connection() as con:
    with con.cursor() as cursor:
      cursor = con.cursor()
      try:
        con.autocommit = False
        cursor.execute("INSERT INTO clase \
                       (id, \
                       nombre_instructor, \
                       horario) VALUES (%s, %s, %s);", (id_clase, 
                                                        nombre_instructor, 
                                                        horario))
        con.commit()
        rowcount = cursor.rowcount > 0
      except(Exception, Error) as error:
          print("\nError: %s\n" % error)
          con.rollback()

  return rowcount > 0

def registrar_asistencia(correo_usuario, id_clase, fecha):
  rowcount = 0
  with connect.get_connection() as con:
    with con.cursor() as cursor:
      cursor = con.cursor()
      try:
        con.autocommit = False
        cursor.execute("INSERT INTO asiste \
                       (correo_miembro, \
                       id_clase, \
                       fecha_asistencia) VALUES (%s, %s, %s);", (correo_usuario, 
                                                        id_clase, 
                                                        fecha))
        con.commit()
        rowcount = cursor.rowcount > 0
      except(Exception, Error) as error:
          print("\nError: %s\n" % error)
          con.rollback()

  return rowcount > 0


def get_datos_clases():
  resultado = None
  with connect.get_connection() as con:
    with con.cursor() as cursor:
      cursor = con.cursor()
      cursor.execute("SELECT id, \
                      nombre_instructor, \
                      horario \
                      FROM clase;");
      resultado = cursor.fetchall()

  if resultado is None:
    resultado = []

  return resultado


def get_datos_asistencias(fecha):
  resultado = None
  with connect.get_connection() as con:
    with con.cursor() as cursor:
      cursor = con.cursor()
      cursor.execute("SELECT m.nombre, \
                      c.id, \
                      a.fecha_asistencia \
                     FROM asiste a \
                     INNER JOIN miembro m ON a.correo_miembro = m.correo_miembro \
                     INNER JOIN clase c ON a.id_clase = c.id \
                     WHERE a.fecha_asistencia = %s;", (fecha, ));
      resultado = cursor.fetchall()

  if resultado is None:
    resultado = []

  return resultado
