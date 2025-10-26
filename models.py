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


class CursoCreate(CursoBase):
    pass
