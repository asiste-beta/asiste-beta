from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from database import get_db
from models import Student
from schemas import StudentCreateSchema, StudentOut
from utils import generar_usuario, hash_contraseña


router = APIRouter(prefix="/students", tags=["Estudiantes"])


@router.get("/", response_model=List[StudentOut])
def listar_estudiantes(db: Session = Depends(get_db)):
    return db.query(Student).all()


@router.post("/", response_model=StudentOut)
def crear_estudiante(
    data: StudentCreateSchema,
    db: Session = Depends(get_db)
):
    existente = (
        db.query(Student)
        .filter(Student.codigo_barras == data.codigo_barras)
        .first()
    )

    if existente:
        raise HTTPException(
            status_code=400,
            detail="Ya existe un estudiante con ese código de barras"
        )

    usuario = generar_usuario(data.nombre, data.codigo_barras)

    nuevo_estudiante = Student(
        nombre=data.nombre,
        grado=data.grado,
        curso=data.curso,
        codigo_barras=data.codigo_barras,
        usuario=usuario,
        # La contraseña inicial del estudiante es su número de documento
        contraseña=hash_contraseña(data.codigo_barras),
    )

    db.add(nuevo_estudiante)
    db.commit()
    db.refresh(nuevo_estudiante)

    return nuevo_estudiante


@router.get("/buscar/{codigo_barras}", response_model=StudentOut)
def buscar_por_codigo(codigo_barras: str, db: Session = Depends(get_db)):
    estudiante = (
        db.query(Student)
        .filter(Student.codigo_barras == codigo_barras)
        .first()
    )

    if not estudiante:
        raise HTTPException(
            status_code=404,
            detail="Estudiante no encontrado"
        )

    return estudiante
