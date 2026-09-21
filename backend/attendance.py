from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from database import get_db
from models import Student, Attendance
from schemas import AttendanceRegisterSchema, AttendanceOut


router = APIRouter(prefix="/attendance", tags=["Asistencia"])


@router.post("/registrar", response_model=AttendanceOut)
def registrar_asistencia(
    data: AttendanceRegisterSchema,
    db: Session = Depends(get_db)
):
    estudiante = (
        db.query(Student)
        .filter(Student.codigo_barras == data.codigo_barras)
        .first()
    )

    if not estudiante:
        raise HTTPException(
            status_code=404,
            detail="Código de barras no reconocido"
        )

    nueva_asistencia = Attendance(student_id=estudiante.id)

    db.add(nueva_asistencia)
    db.commit()
    db.refresh(nueva_asistencia)

    return nueva_asistencia


@router.get("/", response_model=List[AttendanceOut])
def listar_asistencias(db: Session = Depends(get_db)):
    return db.query(Attendance).all()


@router.get("/estudiante/{student_id}", response_model=List[AttendanceOut])
def asistencias_por_estudiante(student_id: int, db: Session = Depends(get_db)):
    return (
        db.query(Attendance)
        .filter(Attendance.student_id == student_id)
        .order_by(Attendance.fecha_asistencia.desc())
        .all()
    )
