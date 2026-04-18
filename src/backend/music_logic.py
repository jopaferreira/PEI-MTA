# Motor - Geração musical procedimental - Calcula intervalos, escalas e tonalidades através de meios tons

import random

# Dicionário expandido (1 oitava inteira + notas agudas para suportar a matemática dos intervalos)
NOTAS_CROMATICAS = [
    {"vexflow": "c/4", "tone": "C4"},   # Índice 0
    {"vexflow": "c#/4", "tone": "C#4"}, # Índice 1
    {"vexflow": "d/4", "tone": "D4"},   # Índice 2
    {"vexflow": "d#/4", "tone": "D#4"}, # Índice 3
    {"vexflow": "e/4", "tone": "E4"},   # Índice 4
    {"vexflow": "f/4", "tone": "F4"},   # Índice 5
    {"vexflow": "f#/4", "tone": "F#4"}, # Índice 6
    {"vexflow": "g/4", "tone": "G4"},   # Índice 7
    {"vexflow": "g#/4", "tone": "G#4"}, # Índice 8
    {"vexflow": "a/4", "tone": "A4"},   # Índice 9
    {"vexflow": "a#/4", "tone": "A#4"}, # Índice 10
    {"vexflow": "b/4", "tone": "B4"},   # Índice 11
    {"vexflow": "c/5", "tone": "C5"},   # Índice 12
    {"vexflow": "c#/5", "tone": "C#5"}, # Índice 13
    {"vexflow": "d/5", "tone": "D5"},   # Índice 14
    {"vexflow": "d#/5", "tone": "D#5"}, # Índice 15
    {"vexflow": "e/5", "tone": "E5"},   # Índice 16
    {"vexflow": "f/5", "tone": "F5"}    # Índice 17
]

def gerar_intervalo_aleatorio():
    """
    Gera duas notas musicais separadas por um intervalo específico calculado matematicamente.
    """
    # Escolhe uma nota base aleatória, limitada ao índice 5 para a 2ª nota não sair da lista
    index_base = random.randint(0, 5)
    nota_base = NOTAS_CROMATICAS[index_base]
    
    # TODOS os intervalos possíveis dentro de uma oitava e a sua distância em meios tons
    tipos_intervalos = {
        "2ª Menor": 1,
        "2ª Maior": 2,
        "3ª Menor": 3,
        "3ª Maior": 4,
        "4ª Perfeita": 5,
        "Trítono": 6,
        "5ª Perfeita": 7,
        "6ª Menor": 8,
        "6ª Maior": 9,
        "7ª Menor": 10,
        "7ª Maior": 11,
        "Oitava": 12
    }
    
    # 1. Sorteia o intervalo CORRETO
    nome_intervalo_correto, meio_tom = random.choice(list(tipos_intervalos.items()))
    
    # Calcula a nota alvo somando os meios tons
    nota_alvo = NOTAS_CROMATICAS[index_base + meio_tom]
    
    # 2. Lógica de múltipla escolha (1 certa + 3 erradas)
    todas_chaves = list(tipos_intervalos.keys())
    todas_chaves.remove(nome_intervalo_correto) # Remove a certa da lista temporariamente
    opcoes_erradas = random.sample(todas_chaves, 3) # Sorteia 3 opções erradas
    
    # Junta a certa com as erradas e baralha tudo
    opcoes_resposta = opcoes_erradas + [nome_intervalo_correto]
    random.shuffle(opcoes_resposta)
    
    # Devolve o exercício estruturado
    return {
        "tipo_exercicio": "Intervalo",
        "detalhe": nome_intervalo_correto,
        "notas": [nota_base, nota_alvo],
        "opcoes": opcoes_resposta
    }