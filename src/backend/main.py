# Motor principal - Geração Musical e de Gravação de Resultados

# Bibliotecas - FastAPI e validação de dados
from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
# Para servir o frontend (HTML/JS) diretamente do backend - RENDER
from fastapi.staticfiles import StaticFiles
# Para navegar no sistema de ficheiros => RENDER
import os
from pydantic import BaseModel

# Bibliotecas - Base de Dados e utilitários
from sqlalchemy.orm import Session, sessionmaker
import random

# Importa modelo da Base de Dados
from models import engine, Tentativa, Utilizador
# Importa função para gerar exercício de tonalidade
from music_logic import gerar_intervalo_aleatorio, gerar_escala_aleatoria, gerar_exercicio_tonalidade 

# Sessões para comunicação com a Base de Dados - SQLite
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

# FUNÇÕES DA API

# Gera Exercício 
@app.get("/api/exercicio/novo")
def gerar_exercicio(filtro: str = "Mistura"): # Recebe o filtro do browser (por defeito é Mistura)
    
    # Decide quais os números que podem ir a sorteio consoante o filtro
    opcoes_validas = []
    if filtro == "Intervalo":
        opcoes_validas = [0]
    elif filtro == "Escala":
        opcoes_validas = [1]
    elif filtro == "Tonalidade":
        opcoes_validas = [2]
    else:
        opcoes_validas = [0, 1, 2] # Se for "Mistura", sorteia entre todos
        
    sorteio = random.choice(opcoes_validas)
    
    if sorteio == 0:
        exercicio = gerar_intervalo_aleatorio()
        mensagem = "Qual é este intervalo?"
    elif sorteio == 1:
        exercicio = gerar_escala_aleatoria()
        mensagem = "Qual é esta escala?"
    else:
        exercicio = gerar_exercicio_tonalidade()
        mensagem = exercicio["mensagem"]
    
    # Constrói a resposta base JSON
    resposta = {
        "status": "sucesso",
        "mensagem": mensagem,
        "tipo_exercicio": exercicio["tipo_exercicio"],
        "detalhe": exercicio["detalhe"],
        "notas": exercicio["notas"],
        "opcoes": exercicio["opcoes"],
        "explicacao": exercicio["explicacao"]
    }
    
    # Injeta os dados da armação de clave se for um exercício de Tonalidade
    if sorteio == 2:
        resposta["num_acidentes"] = exercicio["num_acidentes"]
        resposta["acidentes_ativos"] = exercicio["acidentes_ativos"]
        
    return resposta

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

# SERVIDOR DE FICHEIROS ESTÁTICOS (FRONTEND)
# Encontra a pasta onde ficheiro main.py está => RENDER
caminho_atual = os.path.dirname(os.path.abspath(__file__))
# Constrói o caminho subindo um nível (..) e entrando na pasta frontend => RENDER
caminho_frontend = os.path.join(caminho_atual, "..", "frontend")
# Diz ao FastAPI para servir o index.html a partir da pasta correta => RENDER
app.mount("/", StaticFiles(directory=caminho_frontend, html=True), name="static")