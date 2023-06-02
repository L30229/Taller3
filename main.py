from database import queries
import utils
from enums import OpcionesMenuPrincipal, \
    OpcionesMenuAdmin, \
    OpcionesMenuMiembro, \
    Roles


def get_opciones_menu(menu_enum):
    opciones = ""
    for i, opcion in enumerate(menu_enum, start=1):
        opciones += f"\t{i}) {opcion.name}\n" 

    return opciones


while (True):
    print("\n\t[PANEL PRINCIPAL]\n")
    print(get_opciones_menu(OpcionesMenuPrincipal))
    cantidad_opciones = len(OpcionesMenuPrincipal)
    opcion = int(input(f"Seleccione una opción (1 - {cantidad_opciones}): "))
    while (opcion <= 0 or opcion > cantidad_opciones):
                print()
                print("Opción incorrecta.\n")
                opcion = int(input(f"Seleccione una opción (1 - {cantidad_opciones}): "))

    print()
    match opcion:
        case OpcionesMenuPrincipal.INICIAR_SESION.value:
            correo = input("Ingrese el correo: ")
            contraseña = input("Ingrese la contraseña: ")
            is_cred_correct = queries.is_credenciales_correcta(correo, contraseña)
            while (not is_cred_correct):
                print("\nCredenciales incorrectas.\n")
                correo = input("Ingrese el correo: ")
                contraseña = input("Ingrese la contraseña: ")
                is_cred_correct = queries.is_credenciales_correcta(correo, contraseña)

            print("\nAcceso correcto.\n")
            resultado = queries.get_rol_usuario(correo)
            if resultado is None:
                print("No se encontró ningún rol para el usuario.")
                continue

            rol_usuario = resultado[0]
            match rol_usuario:
                case Roles.ADMINISTRADOR.value:
                    while (True):
                        print("[PANEL ADMIN]")
                        print(get_opciones_menu(OpcionesMenuAdmin))
                        cantidad_opciones = len(OpcionesMenuAdmin)
                        opcion = int(input(f"Seleccione una opción (1 - {cantidad_opciones}): "))
                        while (opcion <= 0 or opcion > cantidad_opciones):
                            print()
                            print("Opción incorrecta.\n")
                            opcion = int(input(f"Seleccione una opción (1 - {cantidad_opciones}): "))

                        print()
                        match opcion:
                            case OpcionesMenuAdmin.REGISTRAR_MIEMBRO.value:
                                print("[" + OpcionesMenuAdmin.REGISTRAR_MIEMBRO.name + "]\n")
                                correo = input("Ingrese correo: ")
                                contraseña = utils.generar_contrasena()
                                nombre = input("Ingrese nombre: ")
                                edad = int(input("Ingrese edad: "))
                                direccion = input("Ingrese dirección: ")
                                telefono = input("Ingrese telefono: ")
                                fecha_vencimiento = input("Ingrese fecha de vencimiento: ")
                                tipo_membresia = input("Ingrese tipo de membresia: ")
                                ingreso = queries.ingresar_miembro(
                                    correo,
                                    contraseña,
                                    nombre,
                                    edad,
                                    direccion,
                                    telefono,
                                    fecha_vencimiento,
                                    tipo_membresia)
                            
                                if (ingreso):
                                    print("\nMiembro ingresado correctamente.\n")
                            
                                else:
                                    print("\nError al ingresar miembro.\n")

                            case OpcionesMenuAdmin.CERRAR_SESION.value:
                                break
                case Roles.MIEMBRO.value:
                    while (True):
                        print("\n\t[PANEL MIEMBRO]\n")
                        print(get_opciones_menu(OpcionesMenuMiembro))
                        cantidad_opciones = len(OpcionesMenuMiembro)
                        opcion = int(input(f"Seleccione una opción (1 - {cantidad_opciones}): "))
                        while (opcion <= 0 or opcion > cantidad_opciones):
                            print()
                            print("Opción incorrecta.\n")
                            opcion = int(input(f"Seleccione una opción (1 - {cantidad_opciones}): "))
                
                        match opcion:
                            case OpcionesMenuMiembro.VER_INFO_PERSONAL.value:
                                pass

                            case OpcionesMenuMiembro.VER_HORARIO_CLASES.value:
                                pass

                            case OpcionesMenuMiembro.REGISTRAR_ASISTENCIA.value:
                                pass

                            case OpcionesMenuMiembro.CERRAR_SESION.value:
                                break

        case OpcionesMenuPrincipal.CERRAR_APLICACION.value:
            print("Aplicación finalizada.")
            break