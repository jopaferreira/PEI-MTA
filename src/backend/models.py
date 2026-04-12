# MODELOS DE DADOS - Define as tabelas e cria a base de dados SQLite.


from sqlalchemy import create_engine, Column, Integer, String, Boolean, DateTime, ForeignKey
from sqlalchemy.orm import declarative_base, relationship
from datetime import datetime

# Configuração da Ligação à Base de Dados - Define o ficheiro local para guardar os dados
SQLALCHEMY_DATABASE_URL = "sqlite:///./teoria_musical.db"

# Motor que comunica com o SQLite ( O argumento 'check_same_thread' como False é uma exigência técnica do FastAPI ao trabalhar com SQLite.)
engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)

# Classe base genérica herdada por todas as tabelas
Base = declarative_base()


# Tabelas

class Utilizador(Base):
    # Tabela que guarda a informação dos alunos/utilizadores.
    __tablename__ = "utilizadores"

    # Colunas da tabela
    id = Column(Integer, primary_key=True, index=True) # Identificador único automático
    username = Column(String, unique=True, index=True) # Nome de utilizador (não podem existir dois iguais)
    data_registo = Column(DateTime, default=datetime.utcnow) # Data e hora da criação do perfil

    # Relação: Um utilizador pode ter muitas 'tentativas' de exercícios
    tentativas = relationship("Tentativa", back_populates="utilizador")


class Tentativa(Base):
    # Tabela que regista o histórico de exercícios resolvidos (Métricas do MVP).
    __tablename__ = "tentativas"

    # Chave primária e ligação ao utilizador (Chave Estrangeira)
    id = Column(Integer, primary_key=True, index=True)
    utilizador_id = Column(Integer, ForeignKey("utilizadores.id"))
    
    # Detalhes do exercício e desempenho
    tipo_exercicio = Column(String, index=True) # Ex: 'Escala', 'Intervalo'
    detalhe = Column(String)                    # Ex: 'Dó Maior', '3ª Menor'
    resposta_dada = Column(String)              # Resposta do utilizador
    correta = Column(Boolean)                   # True se acertou, False se errou
    data_hora = Column(DateTime, default=datetime.utcnow) # Registo temporal da submissão

    # Relação invertida: Esta tentativa pertence a um utilizador específico
    utilizador = relationship("Utilizador", back_populates="tentativas")


# Script de Inicialização
# Só corre se executarmos o ficheiro diretamente no terminal (python models.py).
# Lê as classes e cria o ficheiro físico 'teoria_musical.db' com as colunas certas.
if __name__ == "__main__":
    print("A criar a base de dados SQLite...")
    Base.metadata.create_all(bind=engine)
    print("Base de dados 'teoria_musical.db' criada com sucesso!")