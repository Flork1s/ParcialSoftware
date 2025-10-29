from sqlmodel import SQLModel, Field, Relationship
from typing import Optional, List
from utils import Kind


class CursoBase(SQLModel):
    codigo: int = Field(description="Código único del curso")
    nombre: str
    credito: int
    kind: Kind = Kind.Progamacion
    horario: Optional[str] = None

class Curso(CursoBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    estudiantes: List["Student"] = Relationship(back_populates="curso")

class CursoCreate(CursoBase):
    pass

class CursoUpdate(SQLModel):
    codigo: Optional[int] = None
    nombre: Optional[str] = None
    credito: Optional[int] = None
    kind: Optional[Kind] = None
    horario: Optional[str] = None



class StudentBase(SQLModel):
    cedula: int = Field(primary_key=True, description="Cédula del estudiante")
    nombre: str
    email: str
    semestre: int
    curso_id: Optional[int] = Field(default=None, foreign_key="curso.id")

class Student(StudentBase, table=True):
    curso: Optional[Curso] = Relationship(back_populates="estudiantes")

class StudentCreate(StudentBase):
    pass

class StudentUpdate(SQLModel):
    nombre: Optional[str] = None
    email: Optional[str] = None
    semestre: Optional[int] = None
    curso_id: Optional[int] = None
