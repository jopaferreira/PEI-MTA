# ADR-002 — Escolha do SQLite para Persistência de Dados

**Data:** 12 de abril de 2026
**Estado:** Aceite
**Decisores:** João Paulo Ramos Ferreira

---

## Contexto

O projeto deve permitir a gravação do histórico de resultados para que o utilizador possa consultar as suas métricas posteriormemte. Trata-se de um Produto Mínimo Viável (MVP) focado na demonstração da lógica de aprendizagem, sem necessidade atual de suportar milhares de acessos em simultâneo.

---

## Decisão

Decidi usar **SQLite** gerido através do ORM **SQLAlchemy**.

---

## Alternativas consideradas

| Alternativa | Razão de rejeição |
|------------|------------------|
| PostgreSQL / MySQL | Exigem a instalação de software adicional no sistema operativo ou a configuração de contentores Docker, o que adiciona complexidade desnecessária de infraestrutura para a fase de MVP. |
| Ficheiros JSON estáticos | Não oferecem segurança nem escalabilidade mínima, dificultando a implementação futura de autenticação ou queries mais complexas. |

---

## Consequências

**Positivas:**
- Setup instantâneo, sem configurações adicionais : a base de dados é um simples ficheiro local (`teoria_musical.db`).
- Facilita a partilha do projeto com o orientador e júri, pois basta correr o código Python.
- O uso do ORM SQLAlchemy permite que, no futuro, a troca do SQLite para PostgreSQL exija apenas a alteração de uma linha de código (a *connection string*).

**Negativas / trade-offs:**
- Não é adequado se o projeto escalar para múltiplos acessos simultâneos pesados (bloqueios de escrita).