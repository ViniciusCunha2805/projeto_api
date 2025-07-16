# app/controllers/curso_controller.py

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session, joinedload
from typing import List

from app.db.database import get_db
from app.models.curso import Curso # Importa o modelo Curso
from app.models.aluno import Aluno # Importa o modelo Aluno (para o relacionamento)
from app.schemas.curso_schema import CursoCreate, CursoResponse, CursoUpdate # Importa os schemas de Curso

router = APIRouter(
    prefix="/cursos", # Prefixo para todas as rotas de curso
    tags=["Cursos"]    # Tag para a documentação /docs
)

# CRIAR Curso (POST /cursos/)
@router.post("/", response_model=CursoResponse, status_code=status.HTTP_201_CREATED)
async def create_curso(curso_data: CursoCreate, db: Session = Depends(get_db)):
    # 1. Validação de Nome de Curso Duplicado
    existing_curso = db.query(Curso).filter(Curso.nome == curso_data.nome).first()
    if existing_curso:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Nome do curso já cadastrado")

    # 2. Criação e Persistência no DB
    db_curso = Curso(**curso_data.model_dump())
    db.add(db_curso)
    db.commit()
    db.refresh(db_curso)
    return db_curso

# LISTAR Cursos (GET /cursos/)
@router.get("/", response_model=List[CursoResponse])
async def read_cursos(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    # Consulta todos os cursos com paginação
    # joinedload(Curso.alunos) para pré-carregar os alunos associados, se precisar deles na resposta do curso
    cursos = db.query(Curso).options(joinedload(Curso.alunos)).offset(skip).limit(limit).all()
    return cursos

# BUSCAR Curso por ID (GET /cursos/{curso_id})
@router.get("/{curso_id}", response_model=CursoResponse)
async def read_curso(curso_id: int, db: Session = Depends(get_db)):
    # Busca um curso específico por ID, pré-carregando os alunos
    curso = db.query(Curso).options(joinedload(Curso.alunos)).filter(Curso.id == curso_id).first()
    if not curso:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Curso não encontrado")
    return curso

# ATUALIZAR Curso (PATCH /cursos/{curso_id})
@router.patch("/{curso_id}", response_model=CursoResponse)
async def update_curso(curso_id: int, curso_data: CursoUpdate, db: Session = Depends(get_db)):
    db_curso = db.query(Curso).filter(Curso.id == curso_id).first()
    if not db_curso:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Curso não encontrado")

    # 1. Validação de Nome Duplicado (se nome for atualizado)
    if curso_data.nome is not None and curso_data.nome != db_curso.nome:
        existing_curso_with_name = db.query(Curso).filter(Curso.nome == curso_data.nome).first()
        if existing_curso_with_name:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Nome do curso já cadastrado para outro curso")

    # 2. Atualiza apenas os campos que foram enviados na requisição
    for key, value in curso_data.model_dump(exclude_unset=True).items():
        setattr(db_curso, key, value)

    db.add(db_curso)
    db.commit()
    db.refresh(db_curso)
    return db_curso

# DELETAR Curso (DELETE /cursos/{curso_id})
@router.delete("/{curso_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_curso(curso_id: int, db: Session = Depends(get_db)):
    curso = db.query(Curso).filter(Curso.id == curso_id).first()
    if not curso:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Curso não encontrado")

    # Opcional: Lógica para lidar com alunos matriculados neste curso antes de deletar o curso
    # Por exemplo: setar curso_id para None nos alunos, ou deletar alunos em cascata (se configurado no modelo)
    # Se você configurou `cascade="all, delete-orphan"` no relationship em Curso, os alunos serão deletados.
    # Se não, e se houver alunos com este curso_id, o banco pode impedir a exclusão por causa da Foreign Key.

    db.delete(curso)
    db.commit()
    return # Não retorna conteúdo para 204 No Content