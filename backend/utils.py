from datetime import datetime, time, timezone
from zoneinfo import ZoneInfo

# Todas las horas de la app se piensan en hora de Colombia, sin importar en
# qué servidor corra el proceso (Render corre en UTC).
ZONA_COLOMBIA = ZoneInfo("America/Bogota")


def calcular_estado(fecha_asistencia_utc: datetime, con_excusa: bool = False) -> str:
    """
    Determina el estado de un registro de asistencia a partir de la hora en
    que se escaneó (guardada en la base de datos como UTC "naive").

    Reglas (hora de Colombia):
      - Jornada mañana (registro antes de las 13:00):
          antes de 6:30   -> "a_tiempo"
          6:30 a 6:59     -> "tardanza"
          7:00 en adelante -> "tarde"
      - Jornada tarde (registro a partir de las 13:00):
          antes de 13:00  -> "a_tiempo"
          13:00 a 13:29   -> "tardanza"
          13:30 en adelante -> "tarde"

    Si el registro tiene una excusa asociada, siempre se reporta como
    "justificada", sin importar qué tan tarde haya llegado.
    """
    if con_excusa:
        return "justificada"

    hora_local = (
        fecha_asistencia_utc.replace(tzinfo=timezone.utc)
        .astimezone(ZONA_COLOMBIA)
        .time()
    )

    if hora_local < time(13, 0):
        inicio_jornada = time(6, 30)
        limite_tarde = time(7, 0)
    else:
        inicio_jornada = time(13, 0)
        limite_tarde = time(13, 30)

    if hora_local < inicio_jornada:
        return "a_tiempo"
    if hora_local < limite_tarde:
        return "tardanza"
    return "tarde"


import bcrypt


def hash_contraseña(contraseña: str) -> str:
    """
    Genera el hash de una contraseña con bcrypt.

    bcrypt solo usa los primeros 72 bytes de la contraseña; se trunca a
    propósito para que nunca reviente con documentos o textos largos
    (en vez de usar passlib, que dejó de llevarse bien con las versiones
    nuevas de la librería bcrypt).
    """
    return bcrypt.hashpw(
        contraseña.encode("utf-8")[:72],
        bcrypt.gensalt()
    ).decode("utf-8")


def verificar_contraseña(contraseña: str, hash_guardado: str) -> bool:
    """Compara una contraseña en texto plano contra su hash guardado."""
    return bcrypt.checkpw(
        contraseña.encode("utf-8")[:72],
        hash_guardado.encode("utf-8")
    )


def generar_usuario(nombre_completo: str, documento: str) -> str:
    """
    Genera el nombre de usuario de un estudiante a partir de su nombre
    completo y su número de documento.

    Patrón: primera letra del apellido + primer nombre + documento + "*"
    Ejemplo: "Edwin Martínez", "4917232" -> "medwin4917232*"
    """
    partes = nombre_completo.strip().split()

    if len(partes) == 0:
        raise ValueError("El nombre completo no puede estar vacío")

    nombre = partes[0]
    apellido = partes[-1] if len(partes) > 1 else partes[0]

    return f"{apellido[0].lower()}{nombre.lower()}{documento}*"
