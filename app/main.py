from fastapi import FastAPI

from app.controllers import aluno_controller, curso_controller
from app.db.database import Base, engine

Base.metadata.create_all(bind=engine)

app = FastAPI(title="API da Escola")

app.include_router(aluno_controller.router)
app.include_router(curso_controller.router)