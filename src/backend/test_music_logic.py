# Testes automatizados

import pytest
from music_logic import (
    obter_nota_ortografica,
    gerar_intervalo_aleatorio,
    gerar_escala_aleatoria,
    gerar_exercicio_tonalidade
)

# TESTES MUSICAIS E ORTOGRAFIA
def test_obter_nota_ortografica_diferenciador_enarmonico():
    # Garante que o motor distingue corretamente notas com o mesmo som mas escrita diferente.
    # Testa Dó natural (Som 0, Letra 0='c')
    nota_do = obter_nota_ortografica(0, 0)
    assert nota_do["tone"] == "C4"
    assert nota_do["vexflow"] == "c/4"

    # Testa Fá Sustenido (Som 6, Letra 3='f')
    nota_fa_sust = obter_nota_ortografica(6, 3)
    assert nota_fa_sust["tone"] == "F#4"
    assert nota_fa_sust["vexflow"] == "f#/4"

    # Testa Sol Bemol (Som 6, Letra 4='g') -> Mesmo som que Fá# mas com notação diferente
    nota_sol_bemol = obter_nota_ortografica(6, 4)
    assert nota_sol_bemol["tone"] == "Gb4"
    assert nota_sol_bemol["vexflow"] == "gb/4"

# TESTES DE GERAÇÃO DE INTERVALOS
def test_gerar_intervalo_aleatorio_estrutura():
    # Garante que a geração de intervalos devolve a estrutura e os tipos de dados corretos
    exercicio = gerar_intervalo_aleatorio()
    
    assert exercicio["tipo_exercicio"] == "Intervalo"
    assert len(exercicio["notas"]) == 2  # Um intervalo tem 2 notas
    assert len(exercicio["opcoes"]) == 4 # Têm de existir 4 opções de resposta (1 certa, 3 erradas)
    assert exercicio["detalhe"] in exercicio["opcoes"] # A resposta certa tem de estar nas opções
    assert isinstance(exercicio["explicacao"], str) # Tem de existir uma justificação teórica

# TESTES DE GERAÇÃO DE ESCALAS E MODOS
def test_gerar_escala_aleatoria_estrutura():
    # Garante que as escalas geradas têm 8 notas (1 oitava).
    exercicio = gerar_escala_aleatoria()
    
    assert exercicio["tipo_exercicio"] == "Escala"
    assert len(exercicio["notas"]) == 8  # Todas as escalas diatónicas implementadas têm 8 notas
    assert len(exercicio["opcoes"]) == 4
    assert exercicio["detalhe"] in exercicio["opcoes"]
    
    # Valida formato das notas 
    primeira_nota = exercicio["notas"][0]
    assert "tone" in primeira_nota
    assert "vexflow" in primeira_nota

# TESTES DE GERAÇÃO DE TONALIDADES 
def test_gerar_exercicio_tonalidade_estrutura():
    # Garante que as tonalidades geradas estão contidas nos limites do Ciclo das Quintas.
    exercicio = gerar_exercicio_tonalidade()
    
    assert exercicio["tipo_exercicio"] == "Tonalidade"
    assert -7 <= exercicio["num_acidentes"] <= 7 # O ciclo não excede 7 bemóis ou 7 sustenidos
    assert len(exercicio["opcoes"]) == 4
    assert exercicio["detalhe"] in exercicio["opcoes"]
    assert isinstance(exercicio["acidentes_ativos"], list)
    assert len(exercicio["notas"]) == 0 # Tonalidades testam a armação de clave, não têm notas de pauta