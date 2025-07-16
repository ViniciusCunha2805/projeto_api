from pydantic import BaseModel, EmailStr, Field
from typing import Optional

class AlunoBase(BaseModel):
    nome: str = Field(..., min_length=2, max_length=100)
    idade: Optional[int] = Field(None, gt=0, lt=150)
    email: EmailStr = Field(...)
    curso_id: Optional[int] = None

    class Config:
        from_attributes = True

class AlunoCreate(AlunoBase):
    pass

class AlunoUpdate(BaseModel):
    nome: Optional[str] = Field(None, min_length=2, max_length=100)
    idade: Optional[int] = Field(None, gt=0, lt=150)
    curso_id: Optional[int] = None

    class Config:
        from_attributes = True

class AlunoResponse(AlunoBase):
    id: int

    class Config:
        from_attributes = True