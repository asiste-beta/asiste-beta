"""
Migración de un solo uso: agrega a la tabla `attendance`, que ya existe en
Supabase, las columnas nuevas que usa el sistema de estado de llegada
(con_excusa, motivo_excusa).

`Base.metadata.create_all()` (lo que corre main.py al arrancar) solo crea
tablas que no existen todavía; no modifica una tabla que ya está creada.
Por eso hace falta este script aparte, y solo hay que correrlo una vez.

Uso:
    cd backend
    python migrar_excusas.py
"""

from dotenv import load_dotenv
from sqlalchemy import text

from database import engine

load_dotenv()

COMANDOS = [
    "ALTER TABLE attendance ADD COLUMN IF NOT EXISTS con_excusa BOOLEAN NOT NULL DEFAULT FALSE;",
    "ALTER TABLE attendance ADD COLUMN IF NOT EXISTS motivo_excusa VARCHAR(255);",
]

with engine.begin() as conexion:
    for comando in COMANDOS:
        print(f"Ejecutando: {comando}")
        conexion.execute(text(comando))

print("Listo. La tabla attendance ya tiene las columnas con_excusa y motivo_excusa.")
