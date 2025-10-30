from fastapi import HTTPException
from sqlmodel import Session, select
from models import Curso, CursoCreate, CursoUpdate, Student, StudentCreate, StudentUpdate


def crear_curso(session: Session, data: CursoCreate):
    """
    Crea un nuevo curso.
    Proceso:
        1. Verifica si existe un curso con el mismo código.
        2. Si existe, lanza un error 409.
        3. Si no existe, crea el curso y lo guarda en la base de datos.

    Retorna:
        Curso: El curso creado.
    """
    existente = session.query(Curso).filter(Curso.codigo == data.codigo).first()
    if existente:
        raise HTTPException(status_code=409, detail="Ya existe un curso con ese código")

    curso = Curso(**data.dict())
    session.add(curso)
    session.commit()
    session.refresh(curso)
    return curso


def listar_cursos(session: Session, credito: int = None, codigo: int = None):
    """
      Lista los cursos registrados, con opción de filtrar por crédito o código.
      Retorna:
          list[Curso]: Lista de cursos que coinciden con los filtros.
          Si no se digitan estos campos se ddevuelven todos los cursos registrados.
      """
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
    """
    Obtiene la información de un curso específico por su ID.
    Retorna:
        Curso: Curso encontrado o error 404 si no existe.
    """
    curso = session.get(Curso, curso_id)
    if not curso:
        raise HTTPException(status_code=404, detail="Curso no encontrado")
    return curso


def actualizar_curso(session: Session, curso_id: int, data: CursoUpdate):
    """
    Actualiza los datos de un curso existente.
    Retorna:
        Curso: El curso actualizado.
    """
    curso = session.get(Curso, curso_id)
    if not curso:
        raise HTTPException(status_code=404, detail="Curso no encontrado")

    if data.codigo and data.codigo != curso.codigo:
        existente = session.query(Curso).filter(Curso.codigo == data.codigo).first()
        if existente:
            raise HTTPException(status_code=409, detail="Ya existe un curso con ese código")

    for campo, valor in data.dict(exclude_unset=True).items():
        setattr(curso, campo, valor)
        """ el setattr lo que hace es asignar un valor dinamicamente  que seria un atributo a un objeto
            en este caso serian los datos que se quieren editar si es nombre el campo seria el curso.nombre
            y el valor seria el nuevo digitado y asi lo asigna a cada uno de los campos 
        """

    session.add(curso)
    session.commit()
    session.refresh(curso)
    return curso


def eliminar_curso(session: Session, curso_id: int):
    """
    Elimina un curso por el id de la base de datos y desmatricula a sus estudiantes.
    Retorna:
        Mensaje de confirmación de eliminación.
    """
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
    """
     Lista todos los estudiantes matriculados en un curso por el id del curso.
     Retorna:
         list[Student]: Estudiantes matriculados en el curso.
     """
    curso = session.get(Curso, curso_id)
    if not curso:
        raise HTTPException(status_code=404, detail="Curso no encontrado")

    estudiantes = session.query(Student).filter(Student.curso_id == curso_id).all()
    if not estudiantes:
        raise HTTPException(status_code=404, detail="No hay estudiantes matriculados en este curso")
    return estudiantes



def crear_estudiante(session: Session, data: StudentCreate):
    """
    Crea un nuevo estudiante en la base de datos.
    Retorna:
        Student: Estudiante creado.
    """
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
    """
    Lista todos los estudiantes, con opción de filtrar por semestre si no se digita un semestre se muestran
    todos los estudiantes en la base de datos.
    Retorna:
        list[Student]: Lista de estudiantes encontrados.
    """
    query = session.query(Student)
    if semestre is not None:
        query = query.filter(Student.semestre == semestre)

    estudiantes = query.all()
    if not estudiantes:
        raise HTTPException(status_code=404, detail="No se encontraron estudiantes para ese semestre")
    return estudiantes


def obtener_estudiante(session: Session, cedula: int):
    """
    Obtiene la información de un estudiante por su cédula.
    Retorna:
        Student: Estudiante encontrado.
    """
    estudiante = session.get(Student, cedula)
    if not estudiante:
        raise HTTPException(status_code=404, detail="Estudiante no encontrado")
    return estudiante


def actualizar_estudiante(session: Session, cedula: int, data: StudentUpdate):
    """
    Actualiza los datos de un estudiante.
    Retorna:
        Student: Estudiante actualizado.
    """
    estudiante = session.get(Student, cedula)
    if not estudiante:
        raise HTTPException(status_code=404, detail="Estudiante no encontrado")

    if data.curso_id and estudiante.curso_id and data.curso_id != estudiante.curso_id:
        raise HTTPException(status_code=409, detail="El estudiante ya está matriculado en otro curso")

    for campo, valor in data.dict(exclude_unset=True).items():
        setattr(estudiante, campo, valor)
        """ el setattr lo que hace es asignar un valor dinamicamente  que seria un atributo a un objeto
            en este caso serian los datos que se quieren editar si es nombre el campo seria el estudiante.nombre
            y el valor seria el nuevo digitado y asi lo asigna a cada uno de los campos 
        """

    session.add(estudiante)
    session.commit()
    session.refresh(estudiante)
    return estudiante


def eliminar_estudiante(session: Session, cedula: int):
    """
       Elimina un estudiante de la base de datos en este caso se busca por el id del curso.
       Retorna:
            Mensaje de confirmación de eliminación.
       """
    estudiante = session.get(Student, cedula)
    if not estudiante:
        raise HTTPException(status_code=404, detail="Estudiante no encontrado")

    session.delete(estudiante)
    session.commit()
    return {"mensaje": "Estudiante eliminado correctamente"}


def matricular_estudiante(session: Session, cedula: int, curso_id: int):
    """
    Matricula un estudiante en un curso siempre y cuado la cedula o el id delcurso exista y
    que el estudiante no estre en otro curso ya matriculado.
    Retorna:
        Mensaje de matrícula exitosa.
    """
    estudiante = session.query(Student).filter(Student.cedula == cedula).first()
    if not estudiante:
        raise HTTPException(status_code=404, detail="Estudiante no encontrado")

    curso = session.get(Curso, curso_id)
    if not curso:
        raise HTTPException(status_code=404, detail="Curso no encontrado")

    if estudiante.curso_id is not None and estudiante.curso_id != curso_id:
        raise HTTPException(
            status_code=409,
            detail=f"El estudiante {estudiante.nombre} ya está matriculado en otro curso"
        )

    estudiante.curso_id = curso_id
    session.add(estudiante)
    session.commit()
    session.refresh(estudiante)

    return {
        "mensaje": f"Estudiante {estudiante.nombre} matriculado en {curso.nombre}"
    }



def desmatricular_estudiante(session: Session, cedula: int):
    """
    Desmatricula a un estudiante de su curso actual.
    Retorna:
        Mensaje de confirmación de desmatriculación.
    """
    estudiante = session.get(Student, cedula)
    if not estudiante:
        raise HTTPException(status_code=404, detail="Estudiante no encontrado")

    if not estudiante.curso_id:
        raise HTTPException(status_code=404, detail="El estudiante no está matriculado en ningún curso")

    estudiante.curso_id = None
    session.add(estudiante)
    session.commit()
    session.refresh(estudiante)

    return {"mensaje": f"Estudiante {estudiante.nombre} desmatriculado correctamente"}


def curso_de_estudiante(session: Session, cedula: int):
    """
    Obtiene la información del curso en el que está matriculado un estudiante por la cedula.
    Retorna:
         Información del estudiante y su curso asignado.
    """
    estudiante = session.get(Student, cedula)
    if not estudiante:
        raise HTTPException(status_code=404, detail="Estudiante no encontrado")
    if not estudiante.curso_id:
        raise HTTPException(status_code=404, detail="El estudiante no está matriculado en ningún curso")

    curso = session.exec(select(Curso).where(Curso.id == estudiante.curso_id)).first()
    if not curso:
        raise HTTPException(status_code=404, detail="El curso asignado no existe")

    return {
        "cedula": estudiante.cedula,
        "nombre_estudiante": estudiante.nombre,
        "email": estudiante.email,
        "semestre": estudiante.semestre,
        "curso": {
            "id": curso.id,
            "nombre": curso.nombre,
            "codigo": curso.codigo,
            "credito": curso.credito,
            "horario": curso.horario
        }
    }
