from datetime import datetime

from pydantic import BaseModel, ConfigDict


class LoginSchema(BaseModel):
    usuario: str
    contraseña: str


class StudentCreateSchema(BaseModel):
    nombre: str
    grado: str
    curso: str
    codigo_barras: str  # se usa el número de documento como código de barras


class StudentOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    nombre: str
    grado: str
    curso: str
    codigo_barras: str
    usuario: str


class AttendanceRegisterSchema(BaseModel):
    codigo_barras: str


class AttendanceOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    student_id: int
    fecha_asistencia: datetime
