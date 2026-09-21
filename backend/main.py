from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from database import Base, engine
from auth import router as auth_router
from students import router as students_router
from attendance import router as attendance_router


Base.metadata.create_all(bind=engine)


app = FastAPI(
    title="Asiste Beta",
    description="Sistema de control de asistencia por código de barras",
    version="1.0.0"
)

app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

app.include_router(auth_router)
app.include_router(students_router)
app.include_router(attendance_router)


@app.get("/")
def login_page(request: Request):
    return templates.TemplateResponse(request, "login.html")


@app.get("/panel-estudiante")
def panel_estudiante_page(request: Request):
    return templates.TemplateResponse(request, "panel_estudiante.html")


@app.get("/panel-admin")
def panel_admin_page(request: Request):
    return templates.TemplateResponse(request, "panel_admin.html")
