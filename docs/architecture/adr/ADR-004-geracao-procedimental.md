# ADR-004 — Geração Procedimental vs. Exercícios Estáticos

**Data:** 19 de abril de 2026
**Estado:** Aceite
**Decisores:** João Paulo Ramos Ferreira

---

## Contexto

Para o modo de treino (intervalos e escalas), é necessário definir como os exercícios são apresentados. O sistema precisa de oferecer variedade para que o utilizador não memorize as respostas por repetição.

---

## Decisão

Decidi implementar um **Motor de Geração Procedimental em Python**, que calcula notas, intervalos e escalas em tempo real com base em meios tons e no alfabeto musical, em vez de recorrer a uma base de dados com exercícios pré-escritos.

---

## Alternativas consideradas

| Alternativa | Razão de rejeição |
|------------|------------------|
| Base de Dados com Exercícios Estáticos | Exigiria escrever manualmente dezenas ou centenas de combinações (ex: todas as escalas em todos os tons), tornando o projeto difícil de escalar e manter. |
| Geração apenas por soma de meios tons | Rejeitado por gerar erros ortográficos musicais (ex: apresentar um Lá Sustenido em vez de um Si Bemol numa escala menor), o que prejudicaria a aplicação. |

---

## Consequências

**Positivas:**
- Jogabilidade virtualmente infinita, com exercícios sempre diferentes a cada clique em "Novo Exercício".
- O motor garante a correção ortográfica e teórica das pautas (desenho correto de acidentes e bemóis).
- A base de dados fica dedicada exclusivamente ao histórico de métricas do utilizador, mantendo-se leve.

**Negativas / trade-offs:**
- Aumento da complexidade no Backend.
- Exigiu a criação de dicionários e lógica de mapeamento perturbaram o desenvolvimento da interface.
- Não desenha armações de clave no exercícios com escalas.