from fastapi import FastAPI
from router import router_cursos
from router import router_estudiantes
from database import create_tables

app = FastAPI()

app = FastAPI(lifespan=create_tables, tittle="Gestion Cursos")
app.include_router(router_cursos.router, prefix="/cursos", tags=["Cursos"])
app.include_router(router_estudiantes.router, prefix="/student", tags=["Estudiantes"])


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/hello/{name}")
async def say_hello(name: str):
    return {"message": f"Hello {name}"}
