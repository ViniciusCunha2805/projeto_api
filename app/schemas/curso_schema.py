from pydantic import BaseModel, Field 
from typing import Optional

class CursoBase(BaseModel):
    nome: str = Field(..., min_length=3, max_length=100, description="Nome do curso, deve ser único.")
    descricao: Optional[str] = Field(None, max_length=500, description="Descrição detalhada do curso.")
    ativo: Optional[bool] = Field(True, description="Indica se o curso está ativo. Padrão: True.")

    class Config:
        from_attributes = True # Permite mapear de modelos ORM (SQLAlchemy) para Pydantic

# CursoCreate: Schema para criar um novo Curso (dados de entrada POST)
class CursoCreate(CursoBase):
    pass # Herda todos os campos de CursoBase

# CursoUpdate: Schema para atualizar um Curso (dados de entrada PATCH)
# Todos os campos são opcionais para permitir atualizações parciais.
class CursoUpdate(BaseModel):
    nome: Optional[str] = Field(None, min_length=3, max_length=100, description="Novo nome do curso.")
    descricao: Optional[str] = Field(None, max_length=500, description="Nova descrição do curso.")
    ativo: Optional[bool] = Field(None, description="Status de atividade do curso.")

    class Config:
        from_attributes = True

# CursoResponse: Schema para retornar um Curso (dados de saída GET)
class CursoResponse(CursoBase):
    id: int = Field(..., description="ID único do curso.")
    # Exemplo: Incluir alunos matriculados na resposta
    # from app.schemas.aluno_schema import AlunoResponse # Importe aqui para evitar circularidade
    # alunos: list[AlunoResponse] = [] # Lista de alunos associados a este curso

    class Config:
        from_attributes = True