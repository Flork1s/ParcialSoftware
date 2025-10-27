from fastapi import HTTPException
from sqlmodel import Session
from models import Curso, CursoCreate, CursoUpdate, Student, StudentCreate, StudentUpdate


def crear_curso(session: Session, data: CursoCreate):
    existente = session.query(Curso).filter(Curso.codigo == data.codigo).first()
    if existente:
        raise HTTPException(status_code=409, detail="Ya existe un curso con ese código")

    curso = Curso(**data.dict())
    session.add(curso)
    session.commit()
    session.refresh(curso)
    return curso


def listar_cursos(session: Session, credito: int = None, codigo: int = None):
    query = session.query(Curso)
    if credito is not None:
        query = query.filter(Curso.credito == credito)
    if codigo is not None:
        query = query.filter(Curso.codigo == codigo)

    cursos = query.all()
    if not cursos:
        raise HTTPException(status_code=404, detail="No se encontraron cursos con esos filtros")
    return cursos


def obtener_curso(session: Session, curso_id: int):
    curso = session.get(Curso, curso_id)
    if not curso:
        raise HTTPException(status_code=404, detail="Curso no encontrado")
    return curso


def actualizar_curso(session: Session, curso_id: int, data: CursoUpdate):
    curso = session.get(Curso, curso_id)
    if not curso:
        raise HTTPException(status_code=404, detail="Curso no encontrado")

    if data.codigo and data.codigo != curso.codigo:
        existente = session.query(Curso).filter(Curso.codigo == data.codigo).first()
        if existente:
            raise HTTPException(status_code=409, detail="Ya existe un curso con ese código")

    for campo, valor in data.dict(exclude_unset=True).items():
        setattr(curso, campo, valor)

    session.add(curso)
    session.commit()
    session.refresh(curso)
    return curso


def eliminar_curso(session: Session, curso_id: int):
    curso = session.get(Curso, curso_id)
    if not curso:
        raise HTTPException(status_code=404, detail="Curso no encontrado")

    estudiantes = session.query(Student).filter(Student.curso_id == curso_id).all()
    for est in estudiantes:
        est.curso_id = None
        session.add(est)

    session.delete(curso)
    session.commit()
    return {"mensaje": "Curso eliminado correctamente"}


def estudiantes_en_curso(session: Session, curso_id: int):
    curso = session.get(Curso, curso_id)
    if not curso:
        raise HTTPException(status_code=404, detail="Curso no encontrado")

    estudiantes = session.query(Student).filter(Student.curso_id == curso_id).all()
    if not estudiantes:
        raise HTTPException(status_code=404, detail="No hay estudiantes matriculados en este curso")
    return estudiantes



def crear_estudiante(session: Session, data: StudentCreate):
    existente = session.get(Student, data.cedula)
    if existente:
        raise HTTPException(status_code=409, detail="Ya existe un estudiante con esa cédula")

    if data.curso_id:
        curso = session.get(Curso, data.curso_id)
        if not curso:
            raise HTTPException(status_code=404, detail="El curso especificado no existe")

    estudiante = Student(**data.dict())
    session.add(estudiante)
    session.commit()
    session.refresh(estudiante)
    return estudiante


def listar_estudiantes(session: Session, semestre: int = None):
    query = session.query(Student)
    if semestre is not None:
        query = query.filter(Student.semestre == semestre)

    estudiantes = query.all()
    if not estudiantes:
        raise HTTPException(status_code=404, detail="No se encontraron estudiantes para ese semestre")
    return estudiantes


def obtener_estudiante(session: Session, cedula: int):
    estudiante = session.get(Student, cedula)
    if not estudiante:
        raise HTTPException(status_code=404, detail="Estudiante no encontrado")
    return estudiante


def actualizar_estudiante(session: Session, cedula: int, data: StudentUpdate):
    estudiante = session.get(Student, cedula)
    if not estudiante:
        raise HTTPException(status_code=404, detail="Estudiante no encontrado")

    if data.curso_id and estudiante.curso_id and data.curso_id != estudiante.curso_id:
        raise HTTPException(status_code=409, detail="El estudiante ya está matriculado en otro curso")

    for campo, valor in data.dict(exclude_unset=True).items():
        setattr(estudiante, campo, valor)

    session.add(estudiante)
    session.commit()
    session.refresh(estudiante)
    return estudiante


def eliminar_estudiante(session: Session, cedula: int):
    estudiante = session.get(Student, cedula)
    if not estudiante:
        raise HTTPException(status_code=404, detail="Estudiante no encontrado")

    session.delete(estudiante)
    session.commit()
    return {"mensaje": "Estudiante eliminado correctamente"}


def curso_de_estudiante(session: Session, cedula: int):
    estudiante = session.get(Student, cedula)
    if not estudiante:
        raise HTTPException(status_code=404, detail="Estudiante no encontrado")
    if not estudiante.curso_id:
        raise HTTPException(status_code=404, detail="El estudiante no está matriculado en ningún curso")

    curso = session.get(Curso, estudiante.curso_id)
    if not curso:
        raise HTTPException(status_code=404, detail="El curso asignado no existe")
    return curso



def matricular_estudiante(session: Session, cedula: int, curso_id: int):
    estudiante = session.get(Student, cedula)
    if not estudiante:
        raise HTTPException(status_code=404, detail="Estudiante no encontrado")

    curso = session.get(Curso, curso_id)
    if not curso:
        raise HTTPException(status_code=404, detail="Curso no encontrado")

    if estudiante.curso_id and estudiante.curso_id != curso_id:
        raise HTTPException(status_code=409, detail="El estudiante ya está matriculado en otro curso")

    estudiante.curso_id = curso_id
    session.add(estudiante)
    session.commit()
    session.refresh(estudiante)
    return {"mensaje": f"Estudiante {estudiante.nombre} matriculado en {curso.nombre}"}


def desmatricular_estudiante(session: Session, cedula: int):
    estudiante = session.get(Student, cedula)
    if not estudiante:
        raise HTTPException(status_code=404, detail="Estudiante no encontrado")

    if not estudiante.curso_id:
        raise HTTPException(status_code=404, detail="El estudiante no está matriculado en ningún curso")

    estudiante.curso_id = None
    session.add(estudiante)
    session.commit()
    return {"mensaje": f"Estudiante {estudiante.nombre} desmatriculado correctamente"}
