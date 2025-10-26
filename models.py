from sqlmodel import SQLModel, Relationship, Field
from utils import Kind

class CursoBase(SQLModel):
    id: int | None = Field(description="id curso")
    nombre: str | None = Field(description="nombre curso")
    credito: int | None = Field(description="credito curso")
    kind: Kind | None = Field(description="kind curso", default= Kind.DesarrolloDeSoftware)
    horario: str | None = Field(description="horario curso")

class Curso(CursoBase, table = True):
    id: int | None = Field(default=None, primary_key=True)
    student: list["Student"] = Relationship(back_populates="curso")


class CursoCreate(CursoBase):
    pass

class StudentBase(SQLModel):
    id: int | None = Field(description="cedula estudiante")
    nombre: str | None = Field(description="nombre curso")
    email: str | None = Field(description="email curso")
    semestre: int | None = Field(description="semestre estudiante")

class Student(StudentBase, table = True):
    id: int | None = Field(default=None, primary_key=True)
    curso: list["Curso"] = Relationship(back_populates="student")


class StudentCreate(StudentBase):
    pass
