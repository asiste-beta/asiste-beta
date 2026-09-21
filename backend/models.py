from datetime import datetime

from sqlalchemy import Boolean, Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship

from database import Base


class Student(Base):
    __tablename__ = "students"

    id = Column(Integer, primary_key=True, index=True)

    nombre = Column(String(100), nullable=False)
    grado = Column(String(20), nullable=False)
    curso = Column(String(20), nullable=False)
    codigo_barras = Column(String(100), unique=True, nullable=False, index=True)

    usuario = Column(String(50), unique=True, nullable=False, index=True)
    contraseña = Column(String(255), nullable=False)

    asistencias = relationship(
        "Attendance",
        back_populates="student",
        cascade="all, delete-orphan"
    )


class Admin(Base):
    __tablename__ = "admins"

    id = Column(Integer, primary_key=True, index=True)

    nombre = Column(String(100), nullable=False)
    correo = Column(String(150), unique=True, nullable=False, index=True)
    usuario = Column(String(50), unique=True, nullable=False, index=True)
    contraseña = Column(String(255), nullable=False)

class Attendance(Base):
    __tablename__ = "attendance"

    id = Column(Integer, primary_key=True, index=True)

    student_id = Column(Integer, ForeignKey("students.id"), nullable=False)

    fecha_asistencia = Column(
        DateTime,
        default=datetime.utcnow,
        nullable=False
    )

    # Excepciones: si el estudiante llegó con excusa, el registro se marca
    # como "justificada" sin importar qué tan tarde haya llegado. Se agrega
    # después de registrada la asistencia, desde el panel del administrador.
    con_excusa = Column(Boolean, default=False, nullable=False)
    motivo_excusa = Column(String(255), nullable=True)

    student = relationship(
        "Student",
        back_populates="asistencias"
    )