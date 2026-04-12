# ADR-001 — Escolha de Python e FastAPI para o Backend

**Data:** 12 de abril de 2026
**Estado:** Aceite
**Decisores:** João Paulo Ramos Ferreira (com validação do Orientador)

---

## Contexto

Para o desenvolvimento do "Musical Theory Trainer", é necessário um motor de backend capaz de lidar com a lógica matemática para a geração procedimental de intervalos, escalas e tonalidades. Adicionalmente, a comunicação com a Single Page Application (Frontend) deve ser o mais rápida possível.

---

## Decisão

Decidi usar **Python com a framework FastAPI** para a construção da API REST.

---

## Alternativas consideradas

| Alternativa | Razão de rejeição |
|------------|------------------|
| Node.js / Express | Embora excelente para I/O assíncrono, o Python oferece bibliotecas e uma sintaxe mais limpa e robusta para algoritmos de geração procedimental/matemática complexos. |
| PHP | Considerado inicialmente, mas abandonado por não oferecer o mesmo nível de performance em APIs REST puras e por não alinhar tão bem com as exigências modernas de tipagem estática (Pydantic) que o FastAPI oferece *out-of-the-box*. |

---

## Consequências

**Positivas:**
- Desenvolvimento extremamente rápido graças à geração automática de documentação (Swagger UI).
- Validação de dados nativa e rigorosa à entrada da API utilizando Pydantic.
- Alta performance devido ao uso do servidor ASGI (Uvicorn).

**Negativas / trade-offs:**
- Requer gestão cuidadosa de ambientes virtuais (`venv`) e dependências (`requirements.txt`) para garantir que o projeto corre em qualquer máquina.