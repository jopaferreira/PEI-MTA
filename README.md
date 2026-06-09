# Musical Theory Trainer

> Musical Theory Trainer com Geração Procedimental e Avaliação Automática

**Estudante:** João Paulo Ramos Ferreira · 1800238
**Orientador:** Pedro Pestana  
**UC:** Projecto de Engenharia Informática · Universidade Aberta · 2025/26  
**Repositório:** <https://github.com/jopaferreira/PEI-MTA>

---

## Estado actual

<!-- Actualizar a cada entrega. Escolher um estado e apagar os outros. -->

🟢 **Verde** — A correr regularmente e alinhado com o calendário. O Produto Mínimo Viável (MVP) está concluído. A aplicação encontra-se implementada em ambiente de produção (Render). O foco atual incide sobre a realização de testes funcionais e a redação do Relatório Final.

---

## O que está implementado

<!-- Lista das funcionalidades do MVP que estão funcionais. -->
<!-- Ser específico: não "o login está feito" mas "autenticação por email/password com JWT, sessão persistente em localStorage." -->

- [x] **Estrutura de Base de Dados (SQLite)** — Definição do ORM via SQLAlchemy com as tabelas de Utilizador e Tentativas para suporte à persistência de resultados.
- [x] **Motor da API (Backend)** — Geração procedimental implementada para exercícios de **Intervalos**, **Escalas** e **Tonalidades**.
- [x] **Interface Base (Frontend)** — SPA responsiva com integração do VexFlow (desenho de pautas e acidentes) e Tone.js (reprodução áudio).
- [x] **Justificação Pedagógica** — Apresentação de explicação teórica detalhada após resposta errada.
- [x] **Filtro de Treino** — Possibilidade de o utilizador escolher o tipo de exercício que quer praticar (Mistura, Intervalos, Escalas ou Tonalidades) através de dropdown.
- [x] **Alojamento em Produção** — Servidor FastAPI configurado com resolução de caminhos absolutos (módulo `os`) para servir nativamente os ficheiros estáticos, com a aplicação totalmente alojada e estável na nuvem (Render).
- [x] **Autenticação e Perfis de Utilizador** — Sistema de registo e login com encriptação de passwords (SHA-256), garantindo persistência e isolamento do histórico de métricas (Dashboard) por utilizador.
- [x] **Dashboard detalhado** — Visualização com separação entre a "Sessão Atual" e o "Histórico Global", incluindo gráficos de desempenho por tópico e evolução diária vs. acumulada.
- [x] **Modo de Convidado** — Possibilidade de utilizar a aplicação sem registo, com dados isolados em memória RAM local.
- [x] **Expansão do Motor Procedimental** — Inclusão dos Modos Gregos (Dórico, Frígio, Lídio, Mixolídio e Lócrio).
- [x] **Treino Auditivo Avançado** — Funcionalidade de ocultar a pauta para focar apenas na audição, com possibilidade de seleção do timbre (Som Puro, Jogo Retro, Sopro, Corda, etc.).
- [x] **Testes Unitários e Funcionais** — Bateria de testes automatizados (`pytest`) concluída com 100% de sucesso.

---

## O que está pendente

<!-- O que falta do MVP e porquê. Se algo foi descontinuado, explicar a decisão. -->

O núcleo do Produto Mínimo Viável (MVP) delineado na proposta inicial foi alcançado.
Não existem funcionalidades nucleares pendentes.
O trabalho atual foca-se nas etapas finais do desenvolvimento:

- [x] **Testes Unitários e Funcionais** — Falta recolha de evidências visuais (capturas de ecrã) da interface para o Capítulo 4 do Relatório Final.
- [ ] **Polimento (UI/UX)** — Pequenas afinações estéticas, de margens e responsividade para garantir a melhor experiência possível.

**Funcionalidades transitadas para "Trabalho Futuro":**

- [ ] **Reforço de Segurança Arquitetural:** Substituição do algoritmo de *hashing* (de SHA-256 direto para `bcrypt` com *salt*) e implementação de um sistema robusto de sessões (ex: JWT em *cookies* `HttpOnly`) para mitigar vulnerabilidades de *Insecure Direct Object Reference* (IDOR) detetadas no MVP.

---

## Como instalar e correr

<!-- Instruções que funcionam numa máquina limpa. Se não funcionar na demo, não conta como feito. -->
### ☁️ Acesso em Produção (Recomendado)

A aplicação encontra-se alojada na nuvem e o MVP pode ser avaliado integralmente sem qualquer instalação local através do endereço:
👉 **[https://pei-mta.onrender.com/](https://pei-mta.onrender.com/)**

### 💻 Instalação e Execução Local

**Pré-requisitos:**

- Git

- Python 3.10 ou superior (ambiente de desenvolvimento fixado na versão 3.11.9)

- Browser web moderno

**1. Instalação e Configuração**
Abra o terminal e execute os seguintes comandos:

```bash
# Clonar o repositório
git clone https://github.com/jopaferreira/PEI-MTA.git

# Navegar para a diretoria do backend
cd PEI-MTA/src/backend

# Criar e ativar um ambiente virtual (recomendado)
python -m venv venv
# No Windows: venv\Scripts\activate
# No Mac/Linux: source venv/bin/activate

# Instalar dependências
pip install -r requirements.txt

# Inicializar a Base de Dados (cria o ficheiro teoria_musical.db)
python models.py

# Executar a bateria de testes automatizados (Opcional)
pytest test_music_logic.py -v -p no:cacheprovider
```

**2. Arranque do Sistema Integrado**

```bash
# Iniciar o servidor FastAPI (dentro da pasta src/backend)
uvicorn main:app --reload

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

- Documentação Oficial FastAPI: <https://fastapi.tiangolo.com/>

- Documentação Oficial VexFlow: <https://github.com/0xfe/vexflow>

- Documentação Oficial Tone.js: <https://tonejs.github.io/>

- Documentação SQLAlchemy: <https://www.sqlalchemy.org/>

### Ferramentas de IA utilizadas

<!-- Obrigatório declarar. Não é penalizado. -->

| Ferramenta | Para que foi usada |
|-----------|-------------------|
| Google Gemini | Utilizado como ferramenta de apoio pedagógico para estruturar propostas de arquitetura (modelo C4), gerar código boilerplate inicial e debater boas práticas de separação Frontend/Backend. |
| Claude (Anthropic) | Utilizado como assistente de debugging ao longo do desenvolvimento: resolução de problemas de deployment no Render e lógica de detecção de ambiente (local vs. produção) no frontend. |

---

*Última actualização: 7 de junho de 2026 · Sem. 13*
