from sqlalchemy.orm import Session
from passlib.context import CryptContext

from database import Base, engine
from models import Student, Admin
from utils import generar_usuario


pwd_context = CryptContext(
    schemes=["bcrypt"],
    deprecated="auto"
)


# Crear las tablas si todavía no existen
Base.metadata.create_all(bind=engine)


# Estudiantes iniciales (el código de barras es su número de documento)
students = [
    {"nombre": "Edwin Martínez", "grado": "11", "curso": "05", "documento": "4917232"},
    {"nombre": "Jhon Bohórquez", "grado": "11", "curso": "05", "documento": "1045768394"},
    {"nombre": "Yuriana Osorio", "grado": "11", "curso": "05", "documento": "1043145073"},
]

# Administrador inicial. Cambia esta contraseña después de tu primer ingreso.
admin_data = {
    "nombre": "Administrador",
    "correo": "fjhonson53@gmail.com",
    "usuario": "admin",
    "contraseña": "admin123",
}


with Session(engine) as db:

    for data in students:
        existente = (
            db.query(Student)
            .filter(Student.codigo_barras == data["documento"])
            .first()
        )

        if existente:
            print(f"Ya existe: {data['nombre']}")
            continue

        usuario = generar_usuario(data["nombre"], data["documento"])

        estudiante = Student(
            nombre=data["nombre"],
            grado=data["grado"],
            curso=data["curso"],
            codigo_barras=data["documento"],
            usuario=usuario,
            contraseña=pwd_context.hash(data["documento"]),
        )

        db.add(estudiante)
        print(f"Creado: {data['nombre']} -> usuario: {usuario}")

    admin_existente = (
        db.query(Admin)
        .filter(Admin.correo == admin_data["correo"])
        .first()
    )

    if not admin_existente:
        admin = Admin(
            nombre=admin_data["nombre"],
            correo=admin_data["correo"],
            usuario=admin_data["usuario"],
            contraseña=pwd_context.hash(admin_data["contraseña"]),
        )
        db.add(admin)
        print(f"Creado administrador -> usuario: {admin_data['usuario']} / contraseña: {admin_data['contraseña']}")
    else:
        print("El administrador ya existe")

    db.commit()


print("Listo. Estudiantes y administrador creados correctamente.")
