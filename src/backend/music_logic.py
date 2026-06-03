# Motor - Geração musical procedimental com Ortografia Diatónica

import random

# Constantes para as Tonalidades (Ciclo das Quintas)
ORDEM_SUSTENIDOS = ['F', 'C', 'G', 'D', 'A', 'E', 'B']
ORDEM_BEMOIS = ['B', 'E', 'A', 'D', 'G', 'C', 'F']
# Atribuição do número de acidentes para cada tonalidade 
TONALIDADES_MAIORES = {
    -7: 'Cb Maior', -6: 'Gb Maior', -5: 'Db Maior', -4: 'Ab Maior', -3: 'Eb Maior', -2: 'Bb Maior', -1: 'F Maior',
     0: 'C Maior',
     1: 'G Maior',   2: 'D Maior',   3: 'A Maior',   4: 'E Maior',   5: 'B Maior',   6: 'F# Maior',  7: 'C# Maior'
}

TONALIDADES_MENORES = {
    -7: 'Ab Menor', -6: 'Eb Menor', -5: 'Bb Menor', -4: 'F Menor', -3: 'C Menor', -2: 'G Menor', -1: 'D Menor',
     0: 'A Menor',
     1: 'E Menor',   2: 'B Menor',   3: 'F# Menor',  4: 'C# Menor',  5: 'G# Menor',  6: 'D# Menor',  7: 'A# Menor'
}

# O Dicionário de meios tons
# Atribui a posição do som para a nota correta
DICIONARIO_ORTOGRAFICO = {
    0: {'c': {"vexflow": "c/4", "tone": "C4"}, 'b': {"vexflow": "b#/3", "tone": "B#3"}},
    1: {'c': {"vexflow": "c#/4", "tone": "C#4"}, 'd': {"vexflow": "db/4", "tone": "Db4"}},
    2: {'d': {"vexflow": "d/4", "tone": "D4"}},
    3: {'d': {"vexflow": "d#/4", "tone": "D#4"}, 'e': {"vexflow": "eb/4", "tone": "Eb4"}},
    4: {'e': {"vexflow": "e/4", "tone": "E4"}, 'f': {"vexflow": "fb/4", "tone": "Fb4"}},
    5: {'f': {"vexflow": "f/4", "tone": "F4"}, 'e': {"vexflow": "e#/4", "tone": "E#4"}},
    6: {'f': {"vexflow": "f#/4", "tone": "F#4"}, 'g': {"vexflow": "gb/4", "tone": "Gb4"}},
    7: {'g': {"vexflow": "g/4", "tone": "G4"}},
    8: {'g': {"vexflow": "g#/4", "tone": "G#4"}, 'a': {"vexflow": "ab/4", "tone": "Ab4"}},
    9: {'a': {"vexflow": "a/4", "tone": "A4"}},
    10: {'a': {"vexflow": "a#/4", "tone": "A#4"}, 'b': {"vexflow": "bb/4", "tone": "Bb4"}},
    11: {'b': {"vexflow": "b/4", "tone": "B4"}, 'c': {"vexflow": "cb/5", "tone": "Cb5"}},
    12: {'c': {"vexflow": "c/5", "tone": "C5"}, 'b': {"vexflow": "b#/4", "tone": "B#4"}},
    13: {'c': {"vexflow": "c#/5", "tone": "C#5"}, 'd': {"vexflow": "db/5", "tone": "Db5"}},
    14: {'d': {"vexflow": "d/5", "tone": "D5"}},
    15: {'d': {"vexflow": "d#/5", "tone": "D#5"}, 'e': {"vexflow": "eb/5", "tone": "Eb5"}},
    16: {'e': {"vexflow": "e/5", "tone": "E5"}, 'f': {"vexflow": "fb/5", "tone": "Fb5"}},
    17: {'f': {"vexflow": "f/5", "tone": "F5"}, 'e': {"vexflow": "e#/5", "tone": "E#5"}},
    18: {'f': {"vexflow": "f#/5", "tone": "F#5"}, 'g': {"vexflow": "gb/5", "tone": "Gb5"}},
    19: {'g': {"vexflow": "g/5", "tone": "G5"}},
    20: {'g': {"vexflow": "g#/5", "tone": "G#5"}, 'a': {"vexflow": "ab/5", "tone": "Ab5"}},
    21: {'a': {"vexflow": "a/5", "tone": "A5"}}
}

# Alfabeto musical
SEQUENCIA_LETRAS = ['c', 'd', 'e', 'f', 'g', 'a', 'b']

# Notas limpas para gerar os exercícios
NOTAS_BASE_DISPONIVEIS = [
    {"som": 0, "letra": 0}, # Dó
    {"som": 2, "letra": 1}, # Ré
    {"som": 5, "letra": 3}, # Fá
    {"som": 7, "letra": 4}, # Sol
    {"som": 9, "letra": 5}  # Lá
]

# Função para obter a nota correta a partir do dicionário, usando o indice do som e o indice da letra
def obter_nota_ortografica(indice_absoluto, indice_letra):
    letra_desejada = SEQUENCIA_LETRAS[indice_letra % 7]
    opcoes_som = DICIONARIO_ORTOGRAFICO.get(indice_absoluto, {})
    
    if letra_desejada in opcoes_som:
        return opcoes_som[letra_desejada]
    else:
        return list(opcoes_som.values())[0]

# Função para gerar um exercício de intervalo aleatório
def gerar_intervalo_aleatorio():
    base = random.choice(NOTAS_BASE_DISPONIVEIS)
    
    # Atribui a soma de meios tons e a quantidade de saltos de letra para cada tipo de intervalo
    tipos_intervalos = {
        "2ª Menor": (1, 1), "2ª Maior": (2, 1),
        "3ª Menor": (3, 2), "3ª Maior": (4, 2),
        "4ª Perfeita": (5, 3), "4ª Aumentada": (6, 3), 
        "5ª Perfeita": (7, 4), 
        "6ª Menor": (8, 5), "6ª Maior": (9, 5),
        "7ª Menor": (10, 6), "7ª Maior": (11, 6),
        "Oitava": (12, 7)
    }
    # Sorteia um intervalo e obtém os meios tons e saltos nas letras correspondentes
    nome_intervalo, regras = random.choice(list(tipos_intervalos.items()))
    meios_tons, saltos_letra = regras
    # Calcula as notas base e alvo usando o dicionário ortográfico
    nota_base = obter_nota_ortografica(base["som"], base["letra"])
    nota_alvo = obter_nota_ortografica(base["som"] + meios_tons, base["letra"] + saltos_letra)
    # Gera opções de resposta (distratores) e baralha a ordem
    todas_chaves = list(tipos_intervalos.keys())
    todas_chaves.remove(nome_intervalo)
    opcoes_resposta = random.sample(todas_chaves, 3) + [nome_intervalo]
    random.shuffle(opcoes_resposta)
    
    # Justificação Pedagógica
    explicacao = f"Uma {nome_intervalo} corresponde a uma distância exata de {meios_tons} meios-tons."
    
    return {
        "tipo_exercicio": "Intervalo", "detalhe": nome_intervalo,
        "notas": [nota_base, nota_alvo], "opcoes": opcoes_resposta,
        "explicacao": explicacao 
    }

# Função para gerar um exercício de escala ou modo grego
def gerar_escala_aleatoria():
    base = random.choice(NOTAS_BASE_DISPONIVEIS)
    
    # Padrões de meios-tons a partir da tónica
    tipos_escalas = {
        "Escala Maior (Jónio)": [0, 2, 4, 5, 7, 9, 11, 12],
        "Escala Menor Natural (Eólio)": [0, 2, 3, 5, 7, 8, 10, 12],
        "Escala Menor Harmónica": [0, 2, 3, 5, 7, 8, 11, 12],
        "Modo Dórico": [0, 2, 3, 5, 7, 9, 10, 12],
        "Modo Frígio": [0, 1, 3, 5, 7, 8, 10, 12],
        "Modo Lídio": [0, 2, 4, 6, 7, 9, 11, 12],
        "Modo Mixolídio": [0, 2, 4, 5, 7, 9, 10, 12],
        "Modo Lócrio": [0, 1, 3, 4, 6, 8, 10, 12]
    }
    
    # Sorteia uma escala, obtém o nome e o padrão correspondente
    nome_escala_correta, padrao_meios_tons = random.choice(list(tipos_escalas.items()))
    
    notas_escala = []
    for salto_alfabeto, meios_tons in enumerate(padrao_meios_tons):
        # Avança o som e avança a letra do alfabeto ao longo da escala
        nota = obter_nota_ortografica(base["som"] + meios_tons, base["letra"] + salto_alfabeto)
        notas_escala.append(nota)
        
    # Gera opções de resposta: A certa + 3 distratores aleatórios 
    todas_escalas = list(tipos_escalas.keys())
    todas_escalas.remove(nome_escala_correta)
    opcoes_resposta = random.sample(todas_escalas, 3) + [nome_escala_correta]
    random.shuffle(opcoes_resposta)
    
    # Justificação Pedagógica alargada
    explicacoes_teoricas = {
        "Escala Maior (Jónio)": "O modo Jónio (Escala Maior) tem meios-tons entre o 3º/4º e 7º/8º graus.",
        "Escala Menor Natural (Eólio)": "O modo Eólio (Menor Natural) tem meios-tons entre o 2º/3º e 5º/6º graus.",
        "Escala Menor Harmónica": "A Menor Harmónica eleva o 7º grau da escala menor natural num meio-tom para criar a sensível.",
        "Modo Dórico": "O modo Dórico é uma escala menor com a 6ª maior (meios-tons: 2º/3º e 6º/7º).",
        "Modo Frígio": "O modo Frígio é uma escala menor caracterizada pela sua 2ª menor (meios-tons: 1º/2º e 5º/6º).",
        "Modo Lídio": "O modo Lídio é uma escala maior caracterizada pela sua 4ª aumentada (meios-tons: 4º/5º e 7º/8º).",
        "Modo Mixolídio": "O modo Mixolídio é uma escala maior com a 7ª menor (meios-tons: 3º/4º e 6º/7º).",
        "Modo Lócrio": "O modo Lócrio é o único modo com uma 5ª diminuta (meios-tons: 1º/2º e 4º/5º)."
    }
    
    return {
        "tipo_exercicio": "Escala", "detalhe": nome_escala_correta,
        "notas": notas_escala, "opcoes": opcoes_resposta,
        "explicacao": explicacoes_teoricas[nome_escala_correta]
    }

# Função para gerar um exercício de identificação de tonalidade por armação de clave
def gerar_exercicio_tonalidade():
    # Sorteia uma armação de clave (entre 7 bemóis e 7 sustenidos)
    num_acidentes = random.randint(-7, 7)
    
    # Sorteia a tonalidade: Maior ou Menor
    tipo_pergunta = random.choice(['Maior', 'Menor'])
    
    if tipo_pergunta == 'Maior':
        resposta_certa = TONALIDADES_MAIORES[num_acidentes]
        dicionario_opcoes = TONALIDADES_MAIORES
    else:
        resposta_certa = TONALIDADES_MENORES[num_acidentes]
        dicionario_opcoes = TONALIDADES_MENORES

    # Determina os acidentes da armação de clave para desenho pelo VexFlow
    acidentes_ativos = []
    if num_acidentes > 0:
        acidentes_ativos = [f"{nota}#" for nota in ORDEM_SUSTENIDOS[:num_acidentes]]
    elif num_acidentes < 0:
        acidentes_ativos = [f"{nota}b" for nota in ORDEM_BEMOIS[:abs(num_acidentes)]]

    # Gera opções erradas aleatórias - excluindo a resposta certa
    chaves_erradas = random.sample([k for k in dicionario_opcoes.keys() if k != num_acidentes], 3)
    opcoes = [resposta_certa] + [dicionario_opcoes[k] for k in chaves_erradas]
    # Baralha a ordem dos botões
    random.shuffle(opcoes) 

    # Justificação Pedagógica
    texto_acidentes = "nenhum acidente (Dó Maior / Lá Menor)"
    if num_acidentes > 0:
        texto_acidentes = f"{num_acidentes} sustenido(s)"
    elif num_acidentes < 0:
        texto_acidentes = f"{abs(num_acidentes)} bemol/bemóis"
        
    explicacao = f"De acordo com o Ciclo das Quintas, a tonalidade de {resposta_certa} possui exatamente {texto_acidentes} na armação de clave."
    # Devolve as informações do exercício para o frontend:
    # tipo de exercício, resposta correta, opções de resposta, acidentes e explicação pedagógica
    return {
        "tipo_exercicio": "Tonalidade",
        "detalhe": resposta_certa, 
        "notas": [], 
        "opcoes": opcoes,
        "num_acidentes": num_acidentes,
        "acidentes_ativos": acidentes_ativos,
        "mensagem": f"Qual é a Tonalidade {tipo_pergunta} com esta armação de clave?",
        "explicacao": explicacao
    }