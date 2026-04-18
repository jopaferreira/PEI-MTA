# Motor principal - Geração Musical e de Gravação de Resultados

# Bibliotecas - FastAPI e validação de dados
from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

# Bibliotecas - Base de Dados e utilitários
from sqlalchemy.orm import Session, sessionmaker
import random

# Importa modelo da Base de Dados
from models import engine, Base, Tentativa, Utilizador
from music_logic import gerar_intervalo_aleatorio

# Sessões para comunicação com o SQLite
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Inicializa aplicação
app = FastAPI()

# Configuração CORS: Permite que o Frontend (HTML/JS) comunique com a API sem bloqueios
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Abre e fecha a ligação à base de dados para cada pedido HTTP
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Valida os dados enviados pelo Frontend
class TentativaCreate(BaseModel):
    tipo_exercicio: str
    detalhe: str
    resposta_dada: str
    correta: bool

# ==========================================
# FUNÇÕES DA API
# ==========================================

# Gera Exercício 
@app.get("/api/exercicio/novo")
def gerar_exercicio():
    # Chama o nosso novo motor procedimental!
    exercicio = gerar_intervalo_aleatorio()
    
    return {
        "status": "sucesso",
        "mensagem": f"Qual é este intervalo?",
        "tipo_exercicio": exercicio["tipo_exercicio"],
        "detalhe": exercicio["detalhe"],
        "notas": exercicio["notas"],
        "opcoes": exercicio["opcoes"] # Enviamos as opções de escolha múltipla para o Frontend
    }

# Grava Resposta 
@app.post("/api/tentativas/")
# Grava Resposta 
@app.post("/api/tentativas/")
def guardar_tentativa(tentativa: TentativaCreate, db: Session = Depends(get_db)):
    # Procura o utilizador ("Visitante", ID 1). Se não existir cria-o automaticamente.
    user = db.query(Utilizador).filter(Utilizador.id == 1).first()
    if not user:
        user = Utilizador(username="Visitante")
        db.add(user)
        db.commit()
        db.refresh(user)

    # Mapeia os dados recebidos, após validação, para o modelo do SQLAlchemy
    nova_tentativa = Tentativa(
        utilizador_id=user.id,
        tipo_exercicio=tentativa.tipo_exercicio,
        detalhe=tentativa.detalhe,
        resposta_dada=tentativa.resposta_dada,
        correta=tentativa.correta
    )
    
    # Guarda a tentativa no ficheiro SQLite
    db.add(nova_tentativa)
    db.commit()
    
    return {"status": "sucesso", "mensagem": "Gravado na Base de Dados!"}

# Dashboard de Métricas
@app.get("/api/dashboard/")
def obter_metricas(db: Session = Depends(get_db)):
    # Conta o número de exercícios respondidos pelo utilizador
    total = db.query(Tentativa).count()
    if total == 0:
        return {"total_tentativas": 0, "taxa_acerto_global": 0}
    
    # Conta as respostas certas
    certas = db.query(Tentativa).filter(Tentativa.correta == True).count()
    
    # Calcula a percentagem de sucesso
    taxa = (certas / total) * 100
    
    return {
        "total_tentativas": total,
        "respostas_certas": certas,
        "taxa_acerto_global": round(taxa, 2) # Arredonda o valor a 2 casas decimais
    }