from enum import Enum

class OpcionesMenuPrincipal(Enum):
    INICIAR_SESION = 1
    CERRAR_APLICACION = 2


class OpcionesMenuAdmin(Enum):
    REGISTRAR_MIEMBRO = 1
    VER_INFO_MIEMBRO = 2
    ACTUALIZAR_MEMBRESIA = 3
    VER_MEMBRESIAS_VENCIDAS = 4
    AGREGAR_CLASES = 5
    VER_CLASES = 6
    VER_REGISTRO_ASISTENCIA = 7
    CERRAR_SESION = 8

class OpcionesMenuMiembro(Enum):
    VER_INFO_PERSONAL = 1
    VER_HORARIO_CLASES = 2
    REGISTRAR_ASISTENCIA = 3
    CERRAR_SESION = 4

class Roles(Enum):
    ADMINISTRADOR = 1
    MIEMBRO = 2