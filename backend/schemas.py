from datetime import datetime

from pydantic import BaseModel, ConfigDict, computed_field

from utils import calcular_estado


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


class ExcusaSchema(BaseModel):
    motivo: str


class AttendanceOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    student_id: int
    fecha_asistencia: datetime
    con_excusa: bool
    motivo_excusa: str | None = None

    # Se calcula a partir de fecha_asistencia y con_excusa; no vive en la
    # base de datos, así que si algún día cambian las reglas de horario
    # (utils.calcular_estado) todos los registros existentes se recalculan
    # solos la próxima vez que se consulten.
    @computed_field
    @property
    def estado(self) -> str:
        return calcular_estado(self.fecha_asistencia, self.con_excusa)
