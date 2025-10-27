from fastapi import FastAPI
from database import create_tables
from router.router_estudiantes import router as router_estudiantes
from router.router_cursos import router as router_cursos

app = FastAPI(title="Sistema Universitario")


create_tables()

# Incluye los routers
app.include_router(router_estudiantes)
app.include_router(router_cursos)

@app.get("/")
def root():
    return {"mensaje": "API del sistema universitario funcionando correctamente 🚀"}
