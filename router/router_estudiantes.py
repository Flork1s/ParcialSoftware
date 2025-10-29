from fastapi import APIRouter, status
from database import engine
import crud
from models import Student, StudentCreate, StudentUpdate
from sqlmodel import Session

router = APIRouter(prefix="/estudiantes", tags=["Estudiantes"])

@router.post("/", response_model=Student, status_code=status.HTTP_201_CREATED)
def crear(new_student: StudentCreate):
    with Session(engine) as session:
        return crud.crear_estudiante(session, new_student)

@router.get("/", response_model=list[Student])
def listar(semestre: int = None):
    with Session(engine) as session:
        return crud.listar_estudiantes(session, semestre)

@router.get("/{cedula}", response_model=Student)
def obtener(cedula: int):
    with Session(engine) as session:
        return crud.obtener_estudiante(session, cedula)

@router.patch("/{cedula}", response_model=Student)
def actualizar(cedula: int, datos: StudentUpdate):
    with Session(engine) as session:
        return crud.actualizar_estudiante(session, cedula, datos)

@router.delete("/{cedula}")
def eliminar(cedula: int):
    with Session(engine) as session:
        return crud.eliminar_estudiante(session, cedula)

@router.get("/{cedula}/curso")
def curso_de_estudiante(cedula: int):
    with Session(engine) as session:
        return crud.curso_de_estudiante(session, cedula)


# 🧾 Endpoint para matricular estudiante en un curso
@router.post("/{cedula}/matricular/{curso_id}", status_code=status.HTTP_201_CREATED)
def matricular_estudiante(cedula: int, curso_id: int):
    with Session(engine) as session:
        return crud.matricular_estudiante(session, cedula, curso_id)


@router.post("/{cedula}/desmatricular")
def desmatricular(cedula: int):
    with Session(engine) as session:
        return crud.desmatricular_estudiante(session, cedula)
