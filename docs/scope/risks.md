# Gestão de Riscos

**Projecto:** Musical Theory Trainer com Geração Procedimental e Avaliação Automática
**Versão:** 1.0 · 12 de abril de 2026

---

## Tabela de riscos

<!-- Identificar 3 a 5 riscos reais ao projecto. -->
<!-- Probabilidade: Alta / Média / Baixa -->
<!-- Impacto: Alto / Médio / Baixo -->
<!-- Mitigação: o que se faz para reduzir probabilidade ou impacto -->

| ID | Risco | Probabilidade | Impacto | Mitigação |
|----|-------|--------------|---------|-----------|
| R01 | **Deriva de âmbito (*Scope Creep*):** Aumento não planeado da complexidade dos exercícios (ex: adicionar reconhecimento de acordes complexos ou ditados rítmicos) antes da conclusão do MVP. | Média | Alto | Manter o foco restrito aos 3 tipos de exercícios contratualizados (intervalos, escalas, tonalidades). Qualquer funcionalidade extra só será avaliada após a entrega formal do MVP. |
| R02 | **Dificuldades na integração técnica VexFlow/Tone.js:** Dessincronização entre as notas desenhadas visualmente na pauta e as frequências áudio geradas pelo sintetizador. | Alta | Alto | Separação da lógica de renderização: a API Backend envia a nota num formato padronizado (ex: notação científica "C4") que é lido inequivocamente tanto pelo renderizador SVG (VexFlow) como pelo motor de áudio (Tone.js). |
| R03 | **Complexidade do motor de geração procedimental:** Dificuldade na programação da lógica matemática que garante que um exercício musical gerado aleatoriamente respeita as regras da teoria musical convencional. | Média | Médio | Abordagem incremental: criar primeiro dicionários estáticos com dados validados de exercícios; só depois de o fluxo completo funcionar se substituirá por geração puramente processual/matemática. |
| R04 | **Restrições de Autoplay nos Browsers:** O *browser* bloquear a reprodução automática de áudio (Tone.js) por políticas de segurança. | Alta | Médio | O desenho da interface obriga o utilizador a interagir fisicamente com a página (clique explícito no botão "Tocar") para iniciar o contexto de áudio (*AudioContext*), cumprindo as diretrizes dos navegadores modernos. |
| R05 | **Sistemas de Ficheiros Efémeros na Nuvem:** Perda da base de dados SQLite (histórico) quando a plataforma de alojamento gratuito (Render) reinicia o contentor por inatividade. | Alta | Médio | Aceitação do risco para o MVP: a persistência relacional está funcional e demonstrável numa sessão contínua. Arquitetada a transição futura (alterando apenas a *string* do SQLAlchemy) para um serviço de base de dados PostgreSQL isolado e persistente. |
| R06 | **Vulnerabilidades de Segurança:** A autenticação confia no `userId` do *localStorage* (permitindo manipulação de pedidos) e o *hashing* de passwords usa SHA-256 sem *salt*, sendo frágil a ataques de dicionário. | Alta | Alto | Risco assumido e aceite como limitação arquitetural para o âmbito restrito do MVP académico. Para uma evolução é prioritária a transição para `bcrypt` (com *salts*) e autenticação baseada em JWT (*JSON Web Tokens*) com validação *server-side*. |
| R07 | **Validação no Cliente (Exposição de Respostas):** A API envia a solução correta para o Frontend avaliar a resposta localmente. Isto permite que utilizadores consigam inspecionar o tráfego de rede e ver a solução antes de responder. | Alta | Médio | Aceite e justificado pelo âmbito do MVP: a aplicação é uma ferramenta de Avaliação Formativa (treino autónomo) desenhada para operar de forma *stateless* e ultra-rápida. Não está desenhada para Avaliação Sumativa (exames formais anti-fraude). |
| R08 | **Geração Procedimental Delimitada (Espaço Musical Restrito):** O motor de geração automática está circunscrito a um conjunto controlado de 5 notas base e limites estritos de oitava para garantir a ortografia diatónica correta. Não cobre a totalidade da teoria tonal expandida. | Baixa | Médio | Risco assumido e aceite como limitação do MVP. Esta delimitação garante 100% de precisão pedagógica e legibilidade visual (VexFlow) nas estruturas testadas (intervalos, modos e armações), mitigando a geração de enarmonias absurdas ou impossíveis para alunos iniciantes. |

---

## Histórico de actualização

| Data | Risco | Evento | Estado |
|------|-------|--------|--------|
| 04/04/2026 | Todos | Criação da matriz inicial de riscos para a Entrega 1 | Em curso |
| 23/05/2026 | R05 | Identificação de perda de dados no Render por inatividade (Contentor efémero). | Mitigado/Aceite |
| 31/05/2026 | R02, R03 | Conclusão do MVP e testes funcionais confirmam a estabilidade do motor procedimental e a perfeita sincronia entre a pauta visual e o áudio gerado. | Resolvido |
| 10/06/2026 | R06 | Identificação das falhas de IDOR e Hashing no modelo atual de gestão de utilizadores. | Mitigado/Aceite |
| 10/06/2026 | R07 | Formalização da limitação da validação de respostas no cliente, justificando a arquitetura stateless orientada ao treino autónomo. | Mitigado/Aceite |
| 11/06/2026 | R08 | Formalização da natureza delimitada da geração procedimental, justificando o espaço musical restrito em prol da precisão ortográfica. | Resolvido |
