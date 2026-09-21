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
