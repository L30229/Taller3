from database import queries
import re
import utils
from enums import OpcionesMenuPrincipal, \
    OpcionesMenuAdmin, \
    OpcionesMenuMiembro, \
    Roles

def solicitar_contrasena():
    while True:
        contrasena = input("Ingrese una contraseña: ")
        if re.match(r'^(?=.*[A-Z])(?=.*\d).{6,8}$', contrasena):
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
    fecha_vencimiento = input("Ingrese fecha de vencimiento: ")
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
                if resultado is None:
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