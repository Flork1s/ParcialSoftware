from sqlmodel import SQLModel, Field, Relationship
from typing import Optional, List
from utils import Kind

# --- MODELO CURSO ---
class CursoBase(SQLModel):
    nombre: str
    credito: int
    kind: Kind = Kind.DesarrolloDeSoftware
    horario: Optional[str] = None

class Curso(CursoBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    estudiantes: List["Student"] = Relationship(back_populates="cursos", link_model="Matricula")

class CursoCreate(CursoBase):
    pass

class CursoUpdate(SQLModel):
    nombre: Optional[str] = None
    credito: Optional[int] = None
    kind: Optional[Kind] = None
    horario: Optional[str] = None


# --- MODELO ESTUDIANTE ---
class StudentBase(SQLModel):
    nombre: str
    email: str
    semestre: int

class Student(StudentBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    cursos: List[Curso] = Relationship(back_populates="estudiantes", link_model="Matricula")

class StudentCreate(StudentBase):
    pass

class StudentUpdate(SQLModel):
    nombre: Optional[str] = None
    email: Optional[str] = None
    semestre: Optional[int] = None


# --- TABLA INTERMEDIA (MATRÍCULA) ---
class Matricula(SQLModel, table=True):
    curso_id: int = Field(foreign_key="curso.id", primary_key=True)
    estudiante_id: int = Field(foreign_key="student.id", primary_key=True)
