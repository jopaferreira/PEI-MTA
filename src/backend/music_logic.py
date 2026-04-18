# Motor - Geração musical procedimental com Ortografia Diatónica

import random

# O Dicionário meios tons
# Mapeia a posição do som para a nota correta
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

# Notas base limpas para gerar os exercícios
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

def gerar_intervalo_aleatorio():
    base = random.choice(NOTAS_BASE_DISPONIVEIS)
    
    # Mapeia a soma de meios tons e o avanço no alfabeto exigido!
    tipos_intervalos = {
        "2ª Menor": (1, 1), "2ª Maior": (2, 1),
        "3ª Menor": (3, 2), "3ª Maior": (4, 2),
        "4ª Perfeita": (5, 3), "Trítono": (6, 3), 
        "5ª Perfeita": (7, 4), 
        "6ª Menor": (8, 5), "6ª Maior": (9, 5),
        "7ª Menor": (10, 6), "7ª Maior": (11, 6),
        "Oitava": (12, 7)
    }
    
    nome_intervalo, regras = random.choice(list(tipos_intervalos.items()))
    meios_tons, saltos_letra = regras
    
    nota_base = obter_nota_ortografica(base["som"], base["letra"])
    nota_alvo = obter_nota_ortografica(base["som"] + meios_tons, base["letra"] + saltos_letra)
    
    todas_chaves = list(tipos_intervalos.keys())
    todas_chaves.remove(nome_intervalo)
    opcoes_resposta = random.sample(todas_chaves, 3) + [nome_intervalo]
    random.shuffle(opcoes_resposta)
    
    return {
        "tipo_exercicio": "Intervalo", "detalhe": nome_intervalo,
        "notas": [nota_base, nota_alvo], "opcoes": opcoes_resposta
    }

def gerar_escala_aleatoria():
    base = random.choice(NOTAS_BASE_DISPONIVEIS)
    
    tipos_escalas = {
        "Escala Maior": [0, 2, 4, 5, 7, 9, 11, 12],
        "Escala Menor Natural": [0, 2, 3, 5, 7, 8, 10, 12],
        "Escala Menor Harmónica": [0, 2, 3, 5, 7, 8, 11, 12]
    }
    
    nome_escala_correta, padrao_semitons = random.choice(list(tipos_escalas.items()))
    
    notas_escala = []
    for salto_alfabeto, semitons in enumerate(padrao_semitons):
        # Avança o som e avança a letra do alfabeto ao longo da escala
        nota = obter_nota_ortografica(base["som"] + semitons, base["letra"] + salto_alfabeto)
        notas_escala.append(nota)
        
    opcoes_resposta = list(tipos_escalas.keys())
    random.shuffle(opcoes_resposta)
    
    return {
        "tipo_exercicio": "Escala", "detalhe": nome_escala_correta,
        "notas": notas_escala, "opcoes": opcoes_resposta
    }