from database import SessionDep
from fastapi import APIRouter, HTTPException
from models import CursoBase, Curso, CursoCreate

router = APIRouter()

@router.post("/", response_model=Curso,status_code=201)
async def create_curso(new_curso: CursoCreate, session:SessionDep):
    curso = Curso.model_validate(new_curso)
    session.add(curso)
    session.commit()
    session.refresh(curso)
    return curso



@router.get("/{id}",response_model=Curso)
async def found_curso(curso_id:int, session:SessionDep):
    curso_db = session.get(Curso,curso_id)
    if not(curso_db):
        raise HTTPException(status_code=404, detail="Curso not found")
    return curso_db

@router.get("/",response_model=list[Curso])
async def list_cursos(session:SessionDep):
    cursos = session.query(Curso).all()
    return cursos