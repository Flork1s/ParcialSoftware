from database import SessionDep
from fastapi import APIRouter, HTTPException
from models import StudentBase, Student, StudentCreate

router = APIRouter()

@router.post("/", response_model=Student,status_code=201)
async def create_curso(new_curso: StudentCreate, session:SessionDep):
    curso = Student.model_validate(new_curso)
    session.add(curso)
    session.commit()
    session.refresh(curso)
    return curso



@router.get("/{id}",response_model=Student)
async def found_curso(curso_id:int, session:SessionDep):
    student_db = session.get(Student,curso_id)
    if not(student_db):
        raise HTTPException(status_code=404, detail="Student not found")
    return student_db

@router.get("/",response_model=list[Student])
async def list_students(session:SessionDep):
    students = session.query(Student).all()
    return students