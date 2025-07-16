from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session, joinedload
from typing import List

from app.db.database import get_db
from app.models.aluno import Aluno
from app.models.curso import Curso
from app.schemas.aluno_schema import AlunoCreate, AlunoResponse, AlunoUpdate

router = APIRouter(
    prefix="/alunos", # Todas as rotas aqui começam com /alunos
    tags=["Alunos"]   # Para a documentação /docs
)

# CRIAR Aluno (POST /alunos/)
@router.post("/", response_model=AlunoResponse, status_code=status.HTTP_201_CREATED)
async def create_aluno(aluno_data: AlunoCreate, db: Session = Depends(get_db)):
    # 1. Validação de Email Duplicado
    existing_aluno = db.query(Aluno).filter(Aluno.email == aluno_data.email).first()
    if existing_aluno:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Email já cadastrado")

    # 2. Validação de Curso Existente (se curso_id for fornecido)
    if aluno_data.curso_id:
        existing_curso = db.query(Curso).filter(Curso.id == aluno_data.curso_id).first()
        if not existing_curso:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Curso não encontrado")

    # 3. Criação e Persistência no DB
    db_aluno = Aluno(**aluno_data.model_dump())
    db.add(db_aluno)
    db.commit()
    db.refresh(db_aluno)
    return db_aluno

# LISTAR Alunos (GET /alunos/)
@router.get("/", response_model=List[AlunoResponse])
async def read_alunos(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    # Consulta alunos com paginação e pré-carrega o curso associado
    alunos = db.query(Aluno).options(joinedload(Aluno.curso_associado)).offset(skip).limit(limit).all()
    return alunos

# BUSCAR Aluno por ID (GET /alunos/{aluno_id})
@router.get("/{aluno_id}", response_model=AlunoResponse)
async def read_aluno(aluno_id: int, db: Session = Depends(get_db)):
    aluno = db.query(Aluno).options(joinedload(Aluno.curso_associado)).filter(Aluno.id == aluno_id).first()
    if not aluno:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Aluno não encontrado")
    return aluno

# ATUALIZAR Aluno (PATCH /alunos/{aluno_id})
@router.patch("/{aluno_id}", response_model=AlunoResponse)
async def update_aluno(aluno_id: int, aluno_data: AlunoUpdate, db: Session = Depends(get_db)):
    db_aluno = db.query(Aluno).filter(Aluno.id == aluno_id).first()
    if not db_aluno:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Aluno não encontrado")

    # 1. Validação de Email Duplicado (se email for atualizado)
    if aluno_data.email is not None and aluno_data.email != db_aluno.email:
        existing_aluno_with_email = db.query(Aluno).filter(Aluno.email == aluno_data.email).first()
        if existing_aluno_with_email:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Email já cadastrado para outro aluno")

    # 2. Validação de Curso Existente (se curso_id for atualizado)
    if aluno_data.curso_id is not None and aluno_data.curso_id != db_aluno.curso_id:
        existing_curso = db.query(Curso).filter(Curso.id == aluno_data.curso_id).first()
        if not existing_curso:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Curso não encontrado")

    # 3. Atualiza apenas os campos que foram enviados na requisição
    for key, value in aluno_data.model_dump(exclude_unset=True).items():
        setattr(db_aluno, key, value)

    db.add(db_aluno)
    db.commit()
    db.refresh(db_aluno)
    return db_aluno

# DELETAR Aluno (DELETE /alunos/{aluno_id})
@router.delete("/{aluno_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_aluno(aluno_id: int, db: Session = Depends(get_db)):
    aluno = db.query(Aluno).filter(Aluno.id == aluno_id).first()
    if not aluno:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Aluno não encontrado")

    db.delete(aluno)
    db.commit()
    return # Não retorna conteúdo para 204 No Content