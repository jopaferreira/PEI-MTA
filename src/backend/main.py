# Motor principal - Geração Musical e de Gravação de Resultados

# Bibliotecas - FastAPI e validação de dados
from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
# Para servir o frontend (HTML/JS) diretamente do backend
from fastapi.staticfiles import StaticFiles
# Para definir os modelos de dados usados pela API
from pydantic import BaseModel

# Bibliotecas - Base de Dados e utilitários
from sqlalchemy.orm import Session, sessionmaker
import random
# Para navegar no sistema de ficheiros
import os
# Para criar o hash da password (segurança)  
import hashlib 

# Importa modelo da Base de Dados
from models import engine, Tentativa, Utilizador, Base
# Importa função para gerar exercício de tonalidade
from music_logic import gerar_intervalo_aleatorio, gerar_escala_aleatoria, gerar_exercicio_tonalidade 

# Fundamental para o RENDER: Cria as tabelas na base de dados (se ainda não existirem)
Base.metadata.create_all(bind=engine)

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
    utilizador_id: int
    tipo_exercicio: str
    detalhe: str
    resposta_dada: str
    correta: bool

# LÓGICA DE AUTENTICAÇÃO

# Transforma a password num hash SHA-256 
def encriptar_password(password: str) -> str:
    return hashlib.sha256(password.encode()).hexdigest()
# Registo de Utilizador - Verifica se o username já existe e guarda o hash da password
@app.post("/api/auth/registo")
def registar_utilizador(dados: dict, db: Session = Depends(get_db)):
    username = dados.get("username")
    password = dados.get("password")
    
    if not username or not password:
        return {"status": "erro", "mensagem": "Username e password obrigatórios."}
    
    # Verifica se o utilizador já existe
    existe = db.query(Utilizador).filter(Utilizador.username == username).first()
    if existe:
        return {"status": "erro", "mensagem": "Este nome de utilizador já está em uso."}
    # Cria o novo utilizador com a password encriptada e guarda na base de dados    
    novo_user = Utilizador(username=username, password_hash=encriptar_password(password))
    db.add(novo_user)
    db.commit()
    db.refresh(novo_user)
    return {"status": "sucesso", "id": novo_user.id, "username": novo_user.username}

# Login de Utilizador - Verifica se o username existe e se a password está correta
@app.post("/api/auth/login")
def login_utilizador(dados: dict, db: Session = Depends(get_db)):
    username = dados.get("username")
    password = dados.get("password")
    
    user = db.query(Utilizador).filter(Utilizador.username == username).first()
    # Verifica se o utilizador existe e se a password introduzida é correta
    if not user or user.password_hash != encriptar_password(password):
        return {"status": "erro", "mensagem": "Credenciais inválidas."}
        
    return {"status": "sucesso", "id": user.id, "username": user.username}


# FUNÇÕES DA API MUSICAL
# Gera Exercício 
@app.get("/api/exercicio/novo")
# Recebe os dados do filtro do browser (por defeito é Mistura)
def gerar_exercicio(filtro: str = "Mistura"): 
    # Decide quais os números que podem ir a sorteio consoante o filtro
    opcoes_validas = []
    if filtro == "Intervalo":
        opcoes_validas = [0]
    elif filtro == "Escala":
        opcoes_validas = [1]
    elif filtro == "Tonalidade":
        opcoes_validas = [2]
    else:
        # Se for "Mistura", sorteia entre todos
        opcoes_validas = [0, 1, 2] 
    # Sorteia o tipo de exercício a gerar    
    sorteio = random.choice(opcoes_validas)
    
    if sorteio == 0:
        exercicio = gerar_intervalo_aleatorio()
        mensagem = "Qual é este intervalo?"
    elif sorteio == 1:
        exercicio = gerar_escala_aleatoria()
        # Verifica se o nome da resposta contém a palavra "Modo"
        if "Modo" in exercicio["detalhe"]:
            mensagem = "Qual o modo musical desta escala?"
        else:
            mensagem = "Qual é esta escala?"
    else:
        exercicio = gerar_exercicio_tonalidade()
        mensagem = exercicio["mensagem"]
    
    # Constrói a resposta
    resposta = {
        "status": "sucesso",
        "mensagem": mensagem,
        "tipo_exercicio": exercicio["tipo_exercicio"],
        "detalhe": exercicio["detalhe"],
        "notas": exercicio["notas"],
        "opcoes": exercicio["opcoes"],
        "explicacao": exercicio["explicacao"]
    }
    
    # Envia os dados da armação de clave se for um exercício de Tonalidade
    if sorteio == 2:
        resposta["num_acidentes"] = exercicio["num_acidentes"]
        resposta["acidentes_ativos"] = exercicio["acidentes_ativos"]
    return resposta

# Grava Resposta 
@app.post("/api/tentativas")
def guardar_tentativa(tentativa: TentativaCreate, db: Session = Depends(get_db)):
    # Mapeia os dados recebidos, após validação, para o modelo do SQLAlchemy
    nova_tentativa = Tentativa(
        utilizador_id=tentativa.utilizador_id,
        tipo_exercicio=tentativa.tipo_exercicio,
        detalhe=tentativa.detalhe,
        resposta_dada=tentativa.resposta_dada,
        correta=tentativa.correta
    )
    
    # Guarda a tentativa no ficheiro SQLite
    db.add(nova_tentativa)
    db.commit()
    
    return {"status": "sucesso", "mensagem": "Gravado na Base de Dados!"}

# Dashboard de Métricas melhorado
@app.get("/api/dashboard/{user_id}")
def obter_metricas(user_id: int, db: Session = Depends(get_db)):
    # Ordenar por data - garante cálculo correto da evolução acumulada
    tentativas = db.query(Tentativa).filter(Tentativa.utilizador_id == user_id).order_by(Tentativa.data_hora.asc()).all()
    
    if not tentativas:
        return {"total": 0, "taxa_global": 0, "por_tipo": {}, "evolucao_diaria": []}
    
    total = len(tentativas)
    certas = sum(1 for t in tentativas if t.correta)
    
    # Taxa de acertos desagregada por Tipo
    tipos = {"Intervalo": [0,0], "Escala": [0,0], "Tonalidade": [0,0]}
    diario = {} 
    
    for t in tentativas:
        if t.tipo_exercicio in tipos:
            tipos[t.tipo_exercicio][1] += 1
            if t.correta:
                tipos[t.tipo_exercicio][0] += 1
                
        # Agrupada por dia
        if hasattr(t, 'data_hora') and t.data_hora:
            data_str = t.data_hora.strftime("%Y-%m-%d")
        else:
            data_str = date.today().strftime("%Y-%m-%d") # Fallback
            
        if data_str not in diario:
            diario[data_str] = {"certas_dia": 0, "total_dia": 0}
            
        diario[data_str]["total_dia"] += 1
        if t.correta:
            diario[data_str]["certas_dia"] += 1

    por_tipo = {k: round((v[0]/v[1]*100), 1) if v[1] > 0 else 0 for k, v in tipos.items()}
    
    # Taxa por Dia e Acumulada
    evolucao_diaria = []
    certas_acumuladas = 0
    total_acumulado = 0
    
    for d in sorted(diario.keys()):
        c_dia = diario[d]["certas_dia"]
        t_dia = diario[d]["total_dia"]
        
        # Incrementa acumulado histórico
        certas_acumuladas += c_dia
        total_acumulado += t_dia
        
        taxa_dia = round((c_dia / t_dia * 100), 1) if t_dia > 0 else 0
        taxa_acum = round((certas_acumuladas / total_acumulado * 100), 1) if total_acumulado > 0 else 0
        
        evolucao_diaria.append({
            "data": d, 
            "taxa_dia": taxa_dia,
            "taxa_acumulada": taxa_acum
        })
    
    return {
        "total": total,
        "taxa_global": round((certas / total) * 100, 1),
        "por_tipo": por_tipo,
        "evolucao_diaria": evolucao_diaria
    }

# Hard Reset - apaga todas as tentativas de um utilizador
@app.delete("/api/utilizadores/{user_id}/reset")
def reset_estatisticas(user_id: int, db: Session = Depends(get_db)):
    db.query(Tentativa).filter(Tentativa.utilizador_id == user_id).delete()
    db.commit()
    return {"status": "sucesso", "mensagem": "Estatísticas reiniciadas com sucesso."}

# SERVIDOR DE FICHEIROS
# Encontra a pasta onde ficheiro main.py está
caminho_atual = os.path.dirname(os.path.abspath(__file__))
# Constrói o caminho subindo um nível (..) e entrando na pasta frontend
caminho_frontend = os.path.join(caminho_atual, "..", "frontend")
# Diz ao FastAPI para servir o index.html a partir da pasta correta
app.mount("/", StaticFiles(directory=caminho_frontend, html=True), name="static")