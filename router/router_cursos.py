from fastapi import APIRouter, status
from database import engine
import crud
from models import Curso, CursoCreate, CursoUpdate, Student
from sqlmodel import Session

router = APIRouter(prefix="/cursos", tags=["Cursos"])

@router.post("/", response_model=Curso, status_code=status.HTTP_201_CREATED)
def crear(new_curso: CursoCreate):
    with Session(engine) as session:
        return crud.crear_curso(session, new_curso)

@router.get("/", response_model=list[Curso])
def listar(credito: int = None, codigo: int = None):
    with Session(engine) as session:
        return crud.listar_cursos(session, credito, codigo)

@router.get("/{curso_id}", response_model=Curso)
def obtener(curso_id: int):
    with Session(engine) as session:
        return crud.obtener_curso(session, curso_id)

@router.patch("/{curso_id}", response_model=Curso)
def actualizar(curso_id: int, datos: CursoUpdate):
    with Session(engine) as session:
        return crud.actualizar_curso(session, curso_id, datos)

@router.delete("/{curso_id}")
def eliminar(curso_id: int):
    with Session(engine) as session:
        return crud.eliminar_curso(session, curso_id)

@router.get("/{curso_id}/estudiantes", response_model=list[Student])
def estudiantes_en_curso(curso_id: int):
    with Session(engine) as session:
        return crud.estudiantes_en_curso(session, curso_id)
