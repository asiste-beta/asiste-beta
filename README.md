# ASISTE Beta

Sistema simplificado de control de asistencia por código de barras, con
login diferenciado para estudiante y administrador.

## Antes de empezar

Tu `venv` anterior tenía instaladas cientos de librerías que no
corresponden a este proyecto (parece que se generó con el entorno
global de Python activado en vez de uno virtual). Este zip **no
incluye ninguna carpeta `venv/`** — créala de nuevo así:

```
cd asiste-beta
python -m venv venv
venv\Scripts\activate      (en Windows)
pip install -r requirements.txt
```

Verifica que veas `(venv)` al inicio de la línea de tu terminal antes
de instalar nada.

## Configurar la base de datos

El archivo `.env` ya está incluido con tu `DATABASE_URL` de la nube.
Si cambias de proveedor, solo actualiza esa línea.

## Cargar los datos iniciales

Esto crea las tablas, los 3 estudiantes de ejemplo y el administrador:

```
cd backend
python seed.py
```

Administrador inicial:
- usuario: `admin`
- contraseña: `admin123`
- correo asociado: `fjhonson53@gmail.com`

**Cambia esa contraseña** una vez puedas iniciar sesión (por ahora no
hay pantalla para eso — se puede agregar después).

## Levantar el servidor

```
uvicorn main:app --reload
```

Abre `http://127.0.0.1:8000` en el navegador.

## Estructura

- `main.py` – arranca la app, monta las rutas y las páginas HTML
- `database.py` – conexión a PostgreSQL en la nube
- `models.py` – tablas: Student, Admin, Attendance
- `schemas.py` – validación de datos de entrada/salida
- `auth.py` – login (detecta si es estudiante o admin)
- `students.py` – listar/crear estudiantes
- `attendance.py` – registrar y consultar asistencia
- `utils.py` – genera usuario/contraseña automáticamente para cada estudiante
- `seed.py` – carga los datos iniciales
- `templates/` – páginas HTML (login, panel estudiante, panel admin) y dos piezas
  compartidas: `_head.html` (tema, fuente y CSS) y `_iconos.html` (iconos SVG)
- `static/` – CSS y JS (`comun.js` tiene las utilidades compartidas: peticiones,
  cambio de tema, iconos y mensajes)

## Sobre el escaneo

La asistencia se registra desde el **panel del administrador** usando la
cámara del celular (botón "Abrir cámara"). No hay campo de escritura
manual.

Requisitos para que la cámara funcione:

- La página debe abrirse con **https://** (o `localhost`). Con `http://`
  el navegador bloquea la cámara.
- El navegador debe tener permiso de cámara para el sitio.
- Hace falta internet: la librería `html5-qrcode` se descarga de un CDN
  (unpkg, con jsdelivr como respaldo).

## Diseño

- La interfaz usa **tema oscuro por defecto**. El botón de sol/luna de la barra
  superior cambia al tema claro y el navegador recuerda la elección.
- Los colores están todos como variables al inicio de `static/css/style.css`
  (bloques `:root`): para cambiar la paleta basta con editar ahí.
- Los iconos son SVG (estilo Lucide, licencia ISC) y están en
  `templates/_iconos.html`. Para usar uno en el HTML:
  `<svg class="icono"><use href="#i-camera"></use></svg>`. Para agregar uno
  nuevo, añade otro `<symbol id="i-nombre">` en ese archivo.
