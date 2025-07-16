from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from dotenv import load_dotenv
import os

load_dotenv() # Garante que o .env seja lido

# Tenta carregar a URL completa do Aiven primeiro
SQLALCHEMY_DATABASE_URL = os.getenv("AIVEN_DATABASE_URL")

# Se a URL completa não estiver definida, constrói a partir das variáveis separadas
if not SQLALCHEMY_DATABASE_URL:
    # Removi os defaults, pois com Aiven eles não fariam sentido se não definidos
    # Se estas variáveis não estiverem no .env, serão None
    POSTGRES_USER = os.getenv("POSTGRES_USER")
    POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD")
    POSTGRES_DB = os.getenv("POSTGRES_DB")
    POSTGRES_HOST = os.getenv("POSTGRES_HOST")
    POSTGRES_PORT = os.getenv("POSTGRES_PORT")

    # Verifica se as variáveis essenciais para a URL separada estão presentes
    if not all([POSTGRES_USER, POSTGRES_PASSWORD, POSTGRES_DB, POSTGRES_HOST, POSTGRES_PORT]):
        raise ValueError("Credenciais de banco de dados incompletas no .env ou variáveis de ambiente. Verifique POSTGRES_USER, POSTGRES_PASSWORD, POSTGRES_DB, POSTGRES_HOST, POSTGRES_PORT.")

    SQLALCHEMY_DATABASE_URL = (
        f"postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}"
        f"@{POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_DB}"
    )

# Se mesmo depois de tentar carregar ou construir a URL, ela ainda estiver vazia, levanta um erro
if not SQLALCHEMY_DATABASE_URL:
    raise ValueError("SQLALCHEMY_DATABASE_URL não configurada. Verifique seu .env ou variáveis de ambiente.")

engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
            db.close()