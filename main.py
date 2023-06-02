from database import queries
import utils
from enums import OpcionesMenuPrincipal, \
    OpcionesMenuAdmin, \
    OpcionesMenuMiembro, \
    Roles


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
    nombre = input("Ingrese nombre: ")
    edad = int(input("Ingrese edad: "))
    direccion = input("Ingrese dirección: ")
    telefono = input("Ingrese telefono: ")
    fecha_vencimiento = input("Ingrese fecha de vencimiento: ")
    tipo_membresia = input("Ingrese tipo de membresia: ")
    return queries.ingresar_miembro(
        correo,
        utils.generar_contrasena(),
        nombre,
        edad,
        direccion,
        telefono,
        fecha_vencimiento,
        tipo_membresia)


running = True
while (running):
    mostrar_menu("PANEL PRINCIPAL", OpcionesMenuPrincipal)
    cantidad_opciones = len(OpcionesMenuPrincipal)
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

                case Roles.MIEMBRO.value:
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

        case OpcionesMenuPrincipal.CERRAR_APLICACION.value:
            running = False
            print("Aplicación finalizada.")