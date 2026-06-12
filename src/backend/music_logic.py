# Motor - Geração musical procedimental com Ortografia Diatónica e Distratores Inteligentes

import random

# Constantes para as Tonalidades - Ciclo das Quintas
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

# O Dicionário de meios tons - Atribui a posição do som para a nota correta
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

def formatar_nome_nota(nota_dict):
    # Auxiliar para remover a oitava (ex: C4 -> C, A#5 -> A#)
    return nota_dict["tone"].replace("3", "").replace("4", "").replace("5", "")

# Função para obter a nota correta a partir do dicionário
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
    
    tipos_intervalos = {
        "2ª Menor": (1, 1), "2ª Maior": (2, 1),
        "3ª Menor": (3, 2), "3ª Maior": (4, 2),
        "4ª Perfeita": (5, 3), "4ª Aumentada": (6, 3), 
        "5ª Perfeita": (7, 4), 
        "6ª Menor": (8, 5), "6ª Maior": (9, 5),
        "7ª Menor": (10, 6), "7ª Maior": (11, 6),
        "Oitava": (12, 7)
    }
    
    # Distratores inteligentes para intervalos (Maior vs Menor, Perfeita vs Aumentada)
    distratores_diagnosticos = {
        "2ª Menor": ["2ª Maior", "3ª Menor", "4ª Perfeita"],
        "2ª Maior": ["2ª Menor", "3ª Menor", "3ª Maior"],
        "3ª Menor": ["3ª Maior", "2ª Maior", "4ª Perfeita"],
        "3ª Maior": ["3ª Menor", "4ª Perfeita", "4ª Aumentada"],
        "4ª Perfeita": ["4ª Aumentada", "5ª Perfeita", "3ª Maior"],
        "4ª Aumentada": ["4ª Perfeita", "5ª Perfeita", "6ª Menor"],
        "5ª Perfeita": ["4ª Aumentada", "6ª Menor", "6ª Maior"],
        "6ª Menor": ["6ª Maior", "5ª Perfeita", "7ª Menor"],
        "6ª Maior": ["6ª Menor", "7ª Menor", "5ª Perfeita"],
        "7ª Menor": ["7ª Maior", "6ª Maior", "Oitava"],
        "7ª Maior": ["7ª Menor", "Oitava", "6ª Maior"],
        "Oitava": ["7ª Maior", "7ª Menor", "5ª Perfeita"]
    }
    
    nome_intervalo, regras = random.choice(list(tipos_intervalos.items()))
    meios_tons, saltos_letra = regras
    
    nota_base = obter_nota_ortografica(base["som"], base["letra"])
    nota_alvo = obter_nota_ortografica(base["som"] + meios_tons, base["letra"] + saltos_letra)
    
    # Injeção dos distratores
    opcoes_resposta = distratores_diagnosticos[nome_intervalo] + [nome_intervalo]
    random.shuffle(opcoes_resposta)
    
    n_base = formatar_nome_nota(nota_base)
    n_alvo = formatar_nome_nota(nota_alvo)
    graus_distancia = saltos_letra + 1
    explicacao = (
        f"A distância entre <strong>{n_base}</strong> e <strong>{n_alvo}</strong> é uma <strong>{nome_intervalo}</strong>. "
        f"Verifica que abrange exatamente <strong>{graus_distancia} graus</strong> na pauta (letras consecutivas no alfabeto musical) "
        f"e uma separação acústica de <strong>{meios_tons} meio(s)-tom(ns)</strong>."
    )
    
    return {
        "tipo_exercicio": "Intervalo", "detalhe": nome_intervalo,
        "notas": [nota_base, nota_alvo], "opcoes": opcoes_resposta,
        "explicacao": explicacao 
    }

# Função para gerar um exercício de escala ou modo grego
def gerar_escala_aleatoria():
    base = random.choice(NOTAS_BASE_DISPONIVEIS)
    
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
    
    # Distratores inteligentes para escalas (Agrupamento por familiaridade de modos)
    distratores_diagnosticos = {
        "Escala Maior (Jónio)": ["Modo Lídio", "Modo Mixolídio", "Escala Menor Natural (Eólio)"],
        "Escala Menor Natural (Eólio)": ["Modo Dórico", "Escala Menor Harmónica", "Modo Frígio"],
        "Escala Menor Harmónica": ["Escala Menor Natural (Eólio)", "Modo Dórico", "Modo Frígio"],
        "Modo Dórico": ["Escala Menor Natural (Eólio)", "Modo Frígio", "Modo Mixolídio"],
        "Modo Frígio": ["Escala Menor Natural (Eólio)", "Modo Dórico", "Modo Lócrio"],
        "Modo Lídio": ["Escala Maior (Jónio)", "Modo Mixolídio", "Modo Frígio"],
        "Modo Mixolídio": ["Escala Maior (Jónio)", "Modo Dórico", "Modo Lídio"],
        "Modo Lócrio": ["Modo Frígio", "Escala Menor Natural (Eólio)", "Modo Dórico"]
    }
    
    nome_escala_correta, padrao_meios_tons = random.choice(list(tipos_escalas.items()))
    
    notas_escala = []
    for salto_alfabeto, meios_tons in enumerate(padrao_meios_tons):
        nota = obter_nota_ortografica(base["som"] + meios_tons, base["letra"] + salto_alfabeto)
        notas_escala.append(nota)
        
    opcoes_resposta = distratores_diagnosticos[nome_escala_correta] + [nome_escala_correta]
    random.shuffle(opcoes_resposta)
    
    n = [formatar_nome_nota(nt) for nt in notas_escala]
    
    if nome_escala_correta == "Escala Maior (Jónio)":
        explicacao = f"Na <strong>{nome_escala_correta} de {n[0]}</strong>, os meios-tons estão localizados estritamente entre o 3º/4º graus (<strong>{n[2]}-{n[3]}</strong>) e o 7º/8º graus (<strong>{n[6]}-{n[7]}</strong>)."
    elif nome_escala_correta == "Escala Menor Natural (Eólio)":
        explicacao = f"Na <strong>{nome_escala_correta} de {n[0]}</strong>, os meios-tons estão localizados estritamente entre o 2º/3º graus (<strong>{n[1]}-{n[2]}</strong>) e o 5º/6º graus (<strong>{n[4]}-{n[5]}</strong>)."
    elif nome_escala_correta == "Escala Menor Harmónica":
        explicacao = f"Na <strong>{nome_escala_correta} de {n[0]}</strong>, encontras meios-tons entre o 2º/3º graus (<strong>{n[1]}-{n[2]}</strong>), 5º/6º graus (<strong>{n[4]}-{n[5]}</strong>) e 7º/8º graus (<strong>{n[6]}-{n[7]}</strong>), além do característico intervalo de 2ª Aumentada (3 meios-tons) entre o 6º e 7º graus (<strong>{n[5]}-{n[6]}</strong>)."
    elif nome_escala_correta == "Modo Dórico":
        explicacao = f"No <strong>{nome_escala_correta} de {n[0]}</strong> (escala menor com 6ª Maior), os meios-tons situam-se entre o 2º/3º graus (<strong>{n[1]}-{n[2]}</strong>) e o 6º/7º graus (<strong>{n[5]}-{n[6]}</strong>)."
    elif nome_escala_correta == "Modo Frígio":
        explicacao = f"No <strong>{nome_escala_correta} de {n[0]}</strong> (escala menor com a sua marcante 2ª Menor), os meios-tons encontram-se imediatamente entre o 1º/2º graus (<strong>{n[0]}-{n[1]}</strong>) e o 5º/6º graus (<strong>{n[4]}-{n[5]}</strong>)."
    elif nome_escala_correta == "Modo Lídio":
        explicacao = f"No <strong>{nome_escala_correta} de {n[0]}</strong> (escala maior com 4ª Aumentada), os meios-tons localizam-se entre o 4º/5º graus (<strong>{n[3]}-{n[4]}</strong>) e o 7º/8º graus (<strong>{n[6]}-{n[7]}</strong>)."
    elif nome_escala_correta == "Modo Mixolídio":
        explicacao = f"No <strong>{nome_escala_correta} de {n[0]}</strong> (escala maior com 7ª Menor dominante), os meios-tons encontram-se entre o 3º/4º graus (<strong>{n[2]}-{n[3]}</strong>) e o 6º/7º graus (<strong>{n[5]}-{n[6]}</strong>)."
    else:  # Modo Lócrio
        explicacao = f"No <strong>{nome_escala_correta} de {n[0]}</strong> (modo diminuto com 5ª Diminuta), os meios-tons ocorrem entre o 1º/2º graus (<strong>{n[0]}-{n[1]}</strong>) e o 4º/5º graus (<strong>{n[3]}-{n[4]}</strong>)."
        
    return {
        "tipo_exercicio": "Escala", "detalhe": nome_escala_correta,
        "notas": notas_escala, "opcoes": opcoes_resposta,
        "explicacao": explicacao
    }

# Função para gerar um exercício de identificação de tonalidade por armação de clave
def gerar_exercicio_tonalidade():
    num_acidentes = random.randint(-7, 7)
    tipo_pergunta = random.choice(['Maior', 'Menor'])
    
    if tipo_pergunta == 'Maior':
        resposta_certa = TONALIDADES_MAIORES[num_acidentes]
    else:
        resposta_certa = TONALIDADES_MENORES[num_acidentes]

    acidentes_ativos = []
    if num_acidentes > 0:
        acidentes_ativos = [f"{nota}#" for nota in ORDEM_SUSTENIDOS[:num_acidentes]]
    elif num_acidentes < 0:
        acidentes_ativos = [f"{nota}b" for nota in ORDEM_BEMOIS[:abs(num_acidentes)]]

    # Distratores inteligentes para tonalidades (Erros comuns em Tonalidades)
    opcoes = [resposta_certa]
    
    # Distrator: Tonalidade Relativa (Mesma armação, modo oposto)
    if tipo_pergunta == 'Maior':
        opcoes.append(TONALIDADES_MENORES[num_acidentes])
    else:
        opcoes.append(TONALIDADES_MAIORES[num_acidentes])
        
    # Distrator: Erro de acidente (Ex: Confundir 2 sustenidos com 2 bemóis)
    if tipo_pergunta == 'Maior':
        opcoes.append(TONALIDADES_MAIORES[-num_acidentes])
    else:
        opcoes.append(TONALIDADES_MENORES[-num_acidentes])
        
    # Distrator: Erro de contagem de acidentes(Adicionar/subtrair 1 acidente)
    vizinho = num_acidentes + 1 if num_acidentes < 7 else num_acidentes - 1
    if num_acidentes == 0: 
        vizinho = random.choice([-1, 1])
        
    if tipo_pergunta == 'Maior':
        opcoes.append(TONALIDADES_MAIORES[vizinho])
    else:
        opcoes.append(TONALIDADES_MENORES[vizinho])

    # Remove duplicados (ex: num_acidentes = 0 faz com que o oposto também seja 0)
    opcoes_unicas = list(set(opcoes))
    
    # Preenche com opções aleatórias mistas se faltarem devido a duplicados (Dó Maior / Lá Menor)
    while len(opcoes_unicas) < 4:
        aleatorio = random.choice(list(TONALIDADES_MAIORES.values()) + list(TONALIDADES_MENORES.values()))
        if aleatorio not in opcoes_unicas:
            opcoes_unicas.append(aleatorio)
            
    # Assegura que devolve apenas 4 e baralha
    opcoes_finais = opcoes_unicas[:4]
    random.shuffle(opcoes_finais)

    if num_acidentes == 0:
        texto_acidentes = "<strong>nenhum acidente</strong>"
    elif num_acidentes > 0:
        lista_acid = ", ".join(acidentes_ativos)
        texto_acidentes = f"<strong>{num_acidentes} sustenido(s)</strong> ({lista_acid})"
    else:
        lista_acid = ", ".join(acidentes_ativos)
        texto_acidentes = f"<strong>{abs(num_acidentes)} bemol/bemóis</strong> ({lista_acid})"
        
    explicacao = (
        f"A armação de clave apresentada contém exatamente {texto_acidentes}. "
        f"No Ciclo das Quintas, esta configuração exata define a assinatura de duas tonalidades relativas: "
        f"<strong>{TONALIDADES_MAIORES[num_acidentes]}</strong> (eixo Maior) ou <strong>{TONALIDADES_MENORES[num_acidentes]}</strong> (eixo Menor)."
    )
    
    return {
        "tipo_exercicio": "Tonalidade",
        "detalhe": resposta_certa, 
        "notas": [], 
        "opcoes": opcoes_finais,
        "num_acidentes": num_acidentes,
        "acidentes_ativos": acidentes_ativos,
        "mensagem": f"Qual é a Tonalidade {tipo_pergunta} com esta armação de clave?",
        "explicacao": explicacao
    }