from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from database import get_db
from models import Student, Admin
from schemas import LoginSchema
from utils import verificar_contraseña


router = APIRouter(prefix="/auth", tags=["Autenticación"])


@router.post("/login")
def login(
    data: LoginSchema,
    db: Session = Depends(get_db)
):
    # Buscar primero entre los estudiantes
    estudiante = (
        db.query(Student)
        .filter(Student.usuario == data.usuario)
        .first()
    )

    if estudiante:
        if not verificar_contraseña(data.contraseña, estudiante.contraseña):
            raise HTTPException(
                status_code=401,
                detail="Contraseña incorrecta"
            )

        return {
            "tipo": "estudiante",
            "id": estudiante.id,
            "nombre": estudiante.nombre,
            "grado": estudiante.grado,
            "curso": estudiante.curso,
            "usuario": estudiante.usuario
        }

    # Si no es estudiante, buscar entre administradores
    admin = (
        db.query(Admin)
        .filter(Admin.usuario == data.usuario)
        .first()
    )

    if admin:
        if not verificar_contraseña(data.contraseña, admin.contraseña):
            raise HTTPException(
                status_code=401,
                detail="Contraseña incorrecta"
            )

        return {
            "tipo": "admin",
            "id": admin.id,
            "nombre": admin.nombre,
            "correo": admin.correo,
            "usuario": admin.usuario
        }

    # No existe ningún usuario con ese nombre
    raise HTTPException(
        status_code=401,
        detail="Usuario no encontrado"
    )
