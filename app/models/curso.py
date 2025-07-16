from sqlalchemy import Column, Integer, String, ForeignKey
from app.db.database import Base
from sqlalchemy.orm import relationship

class Curso(Base):
    __tablename__ = "curso"

    id = Column(Integer, primary_key=True, index=True)
    nome_curso = Column(String, nullable=False)
    descricao = Column(String, nullable=True) 
    ativo = Column(bool, default=True)

    alunos = relationship("Aluno", back_populates="curso_associado", cascade="all, delete-orphan")
    