from database import queries
import re
from datetime import datetime
from enums import OpcionesMenuPrincipal, \
    OpcionesMenuAdmin, \
    OpcionesMenuMiembro, \
    Roles


def solicitar_fecha(prompt):
    while True:
        try:
            fecha = input(prompt)
            return datetime.strptime(fecha, '%Y-%m-%d')
        
        except ValueError:
            print("Fecha inválida, inténtelo nuevamente. (%Y-%m-%d)")

def solicitar_contrasena():
    contrasena_regex = re.compile(r'^(?=.*[A-Z])(?=.*\d).{6,8}$')
    while True:
        contrasena = input("Ingrese una contraseña: ")
        if contrasena_regex.match(contrasena):
            return contrasena
        
        print("\nContraseña inválida, inténtelo nuevamente. (Debe tener al menos una letra mayúscula"
              ", un número y tener una longitud de 6 a 8 caracteres)\n")

def mostrar_menu(titulo, opciones_menu):
    print(f"\n\t[{titulo}]\n")
    for opcion in opciones_menu:
        print(f"\t{opcion.value}. {opcion.name}")
    
    print()

def ingresar_opcion(opciones_menu):
    opcion = int(input(f"Seleccione una opción (1 - {len(opciones_menu)}): "))
    while (opcion <= 0 or opcion > len(opciones_menu)):
        print()
        print("Opción incorrecta.\n")
        opcion = int(input(f"Seleccione una opción (1 - {len(opciones_menu)}): "))
    
    print()
    return opcion

def iniciar_sesion():
    correo = input("Ingrese el correo: ")
    contraseña = input("Ingrese la contraseña: ")
    while not queries.is_credenciales_correcta(correo, contraseña):
        print("\nCredenciales incorrectas.\n")
        correo = input("Ingrese el correo: ")
        contraseña = input("Ingrese la contraseña: ")

    print("\nAcceso correcto.\n")
    return correo

def registrar_miembro():
    correo = input("Ingrese correo: ")
    contraseña = solicitar_contrasena()
    nombre = input("Ingrese nombre: ")
    edad = int(input("Ingrese edad: "))
    direccion = input("Ingrese dirección: ")
    telefono = input("Ingrese telefono: ")
    fecha_vencimiento = solicitar_fecha("Ingrese fecha de vencimiento: ")
    tipo_membresia = input("Ingrese tipo de membresia: ")
    return queries.ingresar_miembro(
        correo,
        contraseña,
        nombre,
        edad,
        direccion,
        telefono,
        fecha_vencimiento,
        tipo_membresia)

def get_info_miembro():
    correo_miembro = input("Ingrese correo miembro: ")
    info_miembro = queries.get_datos_miembro(correo_miembro)
    salida = ""
    if len(info_miembro) == 0:
        return salida

    (nombre,
    edad,
    direccion,
    telefono,
    fecha_vencimiento_dt,
    tipo_membresia) = info_miembro
    salida += "Nombre: " + nombre + "\n" \
        + "Edad: " + str(edad) + "\n" \
        + "Dirección: " + direccion + "\n" \
        + "Teléfono: " + telefono + "\n" \
        + "Fecha vencimiento: " + fecha_vencimiento_dt.strftime('%Y-%m-%d') + "\n" \
        + "Tipo membresía: " + tipo_membresia + "\n"

    return salida

def actualizar_membresia():
    correo_miembro = input("Ingrese correo miembro: ")
    info_miembro = queries.get_datos_miembro(correo_miembro)
    if len(info_miembro) == 0:
        return False

    fecha_vencimiento_actual = info_miembro[4]
    membresia_actual = info_miembro[5]
    nueva_fecha_vencimiento = input("Ingrese nueva fecha de vencimiento (vacio = mantener fecha): ")
    nueva_membresia = input("Ingrese nueva membresia (vacio = mantener membresia): ")
    if not nueva_fecha_vencimiento:
        nueva_fecha_vencimiento = fecha_vencimiento_actual

    if not nueva_membresia:
        nueva_membresia = membresia_actual

    return queries.actualizar_membresia(
        correo_miembro, 
        nueva_fecha_vencimiento, 
        nueva_membresia)

def get_miembros_membresia_vencida():
    miembros_membresia_vencida = queries.get_datos_miembros_membresia_venc()
    salida = ""
    for (nombre,
    edad,
    direccion,
    telefono,
    fecha_vencimiento_dt,
    tipo_membresia) in miembros_membresia_vencida:
        salida += "Nombre: " + nombre + "\n" \
        + "Edad: " + str(edad) + "\n" \
        + "Dirección: " + direccion + "\n" \
        + "Teléfono: " + telefono + "\n" \
        + "Fecha vencimiento: " + fecha_vencimiento_dt.strftime('%Y-%m-%d') + "\n" \
        + "Tipo membresía: " + tipo_membresia + "\n\n"
    return salida

def agregar_clases():
    numero_clases = int(input("Ingrese la cantidad de clases que sea agregar: "))
    for _ in range(numero_clases):
        id_clase = input("Ingrese nombre para la clase: ")
        nombre_instructor = input("Ingrese nombre del instructor: ")
        patron_horario = re.compile(r'^\d{2}:\d{2}:\d{2}$')
        horario = input("Ingrese el horario (HH:MM:SS): ")
        while not patron_horario.match(horario):
            print('El formato de hora no es válido. (HH:MM:SS)')
            horario = input("Ingrese el horario (HH:MM:SS): ")
        
        ingreso = queries.agregar_clase(id_clase, nombre_instructor, horario)
        if (ingreso):
            print("\nClase ingresada correctamente.\n")
        else:
            print("\nError al ingresar clase.\n")

def get_info_clases():
    info_clases = queries.get_datos_clases()
    salida = ""
    for (id_clase,
    nombre_instructor,
    horario) in info_clases:
        salida += "\nId clase: " + id_clase + "\n" \
        + "Instructor: " + nombre_instructor + "\n" \
        + "Horario: " + horario.strftime("%H:%M:%S") + "\n\n"
    return salida

def get_asistencia_por_fecha():
    fecha = solicitar_fecha("Ingrese fecha: ")
    info_asistencias = queries.get_datos_asistencias(fecha)
    salida = ""
    for  (nombre_miembro,
    id_clase,
    fecha_asistencia) in info_asistencias:
        salida += "\nMiembro: " + nombre_miembro + "\n" \
            + "Id clase: " + id_clase + "\n" \
            + "Fecha asistencia: " + fecha_asistencia.strftime('%Y-%m-%d') + "\n"
    return salida

def subpanel_admin():
    is_logged_admin = True
    while (is_logged_admin):
        mostrar_menu("PANEL ADMIN", OpcionesMenuAdmin)
        opcion = ingresar_opcion(OpcionesMenuAdmin)
        match opcion:
            case OpcionesMenuAdmin.REGISTRAR_MIEMBRO.value:
                print("[" + OpcionesMenuAdmin.REGISTRAR_MIEMBRO.name + "]\n")
                ingreso = registrar_miembro()
                if (ingreso):
                    print("\nMiembro ingresado correctamente.\n")
                else:
                    print("\nError al ingresar miembro.\n")

            case OpcionesMenuAdmin.VER_INFO_MIEMBRO.value:
                print("[" + OpcionesMenuAdmin.VER_INFO_MIEMBRO.name + "]\n")
                info_miembro = get_info_miembro()
                if info_miembro:
                    print(info_miembro)
                else:
                    print("Error al obtener información. (miembro no existe)")

            case OpcionesMenuAdmin.ACTUALIZAR_MEMBRESIA.value:
                print("[" + OpcionesMenuAdmin.ACTUALIZAR_MEMBRESIA.name + "]\n")
                actualizado = actualizar_membresia()
                if actualizado:
                    print("Miembro actualizado correctamente.")
                else:
                    print("Error al actualizar miembro. (miembro no existe o/y datos incorrectos)")

            case OpcionesMenuAdmin.VER_MEMBRESIAS_VENCIDAS.value:
                print("[" + OpcionesMenuAdmin.VER_MEMBRESIAS_VENCIDAS.name + "]\n")
                miembros_membresia_vencida = get_miembros_membresia_vencida()
                if miembros_membresia_vencida:
                    print(miembros_membresia_vencida)
                else:
                    print()
                    print("No hay miembros con membresía vencida.")

            case OpcionesMenuAdmin.AGREGAR_CLASES.value:
                #PENDIENTE: COMPROBAR QUE UN INSTRUCTOR NO HAGA DOS CLASE A LA MISMA HORA.
                print("[" + OpcionesMenuAdmin.AGREGAR_CLASES.name + "]\n")
                agregar_clases()

            case OpcionesMenuAdmin.VER_CLASES.value:
                print("[" + OpcionesMenuAdmin.VER_CLASES.name + "]\n")
                info_clases = get_info_clases()
                if info_clases:
                    print(info_clases)
                else:
                    print()
                    print("No hay clases disponibles.")

            case OpcionesMenuAdmin.VER_REGISTRO_ASISTENCIA.value:
                print("[" + OpcionesMenuAdmin.VER_REGISTRO_ASISTENCIA.name + "]\n")
                info_asistencias = get_asistencia_por_fecha()
                if info_asistencias:
                    print(info_asistencias)
                else:
                    print()
                    print("No hubo ningún miembro presente en esa fecha específica")

            case OpcionesMenuAdmin.CERRAR_SESION.value:
                is_logged_admin = False


def subpanel_miembro():
    is_logged_miembro = True
    while (is_logged_miembro):
        mostrar_menu("PANEL MIEMBRO", OpcionesMenuMiembro)
        opcion = ingresar_opcion(OpcionesMenuMiembro)
        match opcion:
            case OpcionesMenuMiembro.VER_INFO_PERSONAL.value:
                pass

            case OpcionesMenuMiembro.VER_HORARIO_CLASES.value:
                pass

            case OpcionesMenuMiembro.REGISTRAR_ASISTENCIA.value:
                pass

            case OpcionesMenuMiembro.CERRAR_SESION.value:
                is_logged_miembro = False

def panel_principal():
    running = True
    while (running):
        mostrar_menu("PANEL PRINCIPAL", OpcionesMenuPrincipal)
        opcion = ingresar_opcion(OpcionesMenuPrincipal)
        match opcion:
            case OpcionesMenuPrincipal.INICIAR_SESION.value:
                correo_usuario = iniciar_sesion()
                resultado = queries.get_rol_usuario(correo_usuario)
                if len(resultado) == 0:
                    print("No se encontró ningún rol para el usuario.")
                    continue

                rol_usuario = resultado[0]
                match rol_usuario:
                    case Roles.ADMINISTRADOR.value:
                        subpanel_admin()

                    case Roles.MIEMBRO.value:
                        subpanel_miembro()

            case OpcionesMenuPrincipal.CERRAR_APLICACION.value:
                running = False
                print("Aplicación finalizada.")


if __name__ == "__main__":
    panel_principal()