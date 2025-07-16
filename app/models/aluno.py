from sqlalchemy import Column, Integer, String, ForeignKey
from app.db.database import Base
from sqlalchemy.orm import relationship

class Aluno(Base):
    __tablename__ = "alunos"

    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String, nullable=False)
    idade = Column(Integer, nullable=False)
    
    curso_id = Column(Integer, ForeignKey("cursos.id"), nullable=True)
    curso_associado = relationship("Curso", back_populates="alunos")