# Musical Theory Trainer

> Musical Theory Trainer com Geração Procedimental e Avaliação Automática

**Estudante:** João Paulo Ramos Ferreira · 1800238
**Orientador:** Pedro Pestana  
**UC:** Projecto de Engenharia Informática · Universidade Aberta · 2025/26  
**Repositório:** https://github.com/jopaferreira/PEI-MTA 

---

## Estado actual

<!-- Actualizar a cada entrega. Escolher um estado e apagar os outros. -->

🟢 **Verde** — A correr conforme planeado. O repositório foi configurado, a arquitetura base (SPA + API) está estabelecida e o modelo de dados inicial implementado.

---

## O que está implementado

<!-- Lista das funcionalidades do MVP que estão funcionais. -->
<!-- Ser específico: não "o login está feito" mas "autenticação por email/password com JWT, sessão persistente em localStorage." -->

- [x] **Estrutura de Base de Dados (SQLite)** — Definição do ORM via SQLAlchemy com as tabelas de Utilizador e Tentativas para suporte à persistência de resultados.
- [x] **Motor da API (Backend)** — Geração procedimental implementada para exercícios de **Intervalos** e **Escalas**.
- [x] **Interface Base (Frontend)** — SPA responsiva com integração do VexFlow (desenho de pautas e acidentes) e Tone.js (reprodução áudio).

---

## O que está pendente

<!-- O que falta do MVP e porquê. Se algo foi descontinuado, explicar a decisão. -->

- [ ] **Exercícios de Tonalidades** — Implementação da geração procedimental de armações de clave no Backend (Previsto para Semanas 9-10).
- [ ] **Filtro de Exercícios** — Adição de controlos na interface para o utilizador poder escolher o tipo de treino desejado (Previsto para Semanas 9-10).
- [ ] **Sistema de Interação e Avaliação** — Lógica para apresentação de justificação pedagógica em ecrã após resposta errada.

---

## Como instalar e correr

<!-- Instruções que funcionam numa máquina limpa. Se não funcionar na demo, não conta como feito. -->

### Pré-requisitos

```text
- Python 3.10 ou superior (ambiente de desenvolvimento fixado na versão 3.11.9)
- Browser web moderno (Chrome, Firefox, Edge)
```

### Instalação

```bash
# 1. Clonar o repositório
git clone [https://github.com/jopaferreira/PEI-MTA.git](https://github.com/jopaferreira/PEI-MTA.git)
cd PEI-MTA

# 2. Configurar o Backend e instalar dependências
cd src/backend
pip install -r requirements.txt

# 3. Inicializar a Base de Dados
# (Isto irá gerar o ficheiro teoria_musical.db na pasta backend)
python models.py
```

### Acesso

```
# 1. Iniciar o servidor da API (no terminal, dentro da pasta src/backend)
uvicorn main:app --reload

# A API ficará acessível em: [http://127.0.0.1:8000](http://127.0.0.1:8000)
# Documentação interativa (Swagger): [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)

# 2. Iniciar a Interface (Frontend)
Abrir o ficheiro `src/frontend/index.html` diretamente no browser ou utilizar uma extensão como o "Live Server" no VS Code.

```

---

## Decisões de arquitectura principais

<!-- 2 a 4 decisões relevantes com justificação breve. Para o detalhe completo, ver docs/architecture/adr/. -->

| Decisão | Alternativa considerada | Razão da escolha |
|---------|------------------------|-----------------|
| Python + FastAPI (Backend) | Node.js / Express | Permite criar uma API REST extremamente rápida, separada do frontend, ideal para lidar com a computação pesada e geração procedimental musical sem bloquear o browser. |
| SQLite (Base de Dados) | PostgreSQL / MySQL | Relacional, leve e integrado no próprio sistema de ficheiros. Ideal para persistir o histórico de métricas no MVP sem necessidade de infraestrutura externa complexa. |
| SPA com VexFlow e Tone.js | Aplicação Nativa (Mobile) | Garante fluidez e acessibilidade via browser. O VexFlow é o standard web para notação vetorial precisa (SVG) e o Tone.js evita a necessidade de servir ficheiros estáticos pesados (MP3). |


---

## Referências e IA utilizada

<!-- Bibliotecas, APIs externas, tutoriais seguidos. -->
<!-- Distinguir o que foi escrito de raiz do que foi adaptado ou gerado. -->

### Referências técnicas

- Documentação Oficial FastAPI: https://fastapi.tiangolo.com/

- Documentação Oficial VexFlow: https://github.com/0xfe/vexflow

- Documentação Oficial Tone.js: https://tonejs.github.io/

- Documentação SQLAlchemy: https://www.sqlalchemy.org/

### Ferramentas de IA utilizadas

<!-- Obrigatório declarar. Não é penalizado. -->

| Ferramenta | Para que foi usada |
|-----------|-------------------|
| Google Gemini | Utilizado como ferramenta de apoio pedagógico para estruturar propostas de arquitetura (modelo C4), gerar código boilerplate inicial e debater boas práticas de separação Frontend/Backend. |

---

*Última actualização: 19 de abril de 2026 · Sem. 5*
