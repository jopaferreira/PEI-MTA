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

---

## Histórico de actualização

| Data | Risco | Evento | Estado |
|------|-------|--------|--------|
| 04/04/2026 | Todos | Criação da matriz inicial de riscos para a Entrega 1 | Em curso |
