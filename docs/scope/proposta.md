# Proposta de Projecto

**Título:** Musical Theory Trainer com Geração Procedimental e Avaliação Automática 
**Estudante:** João Paulo Ramos Ferreira· 1800238  
**Orientador:** Pedro Pestana  
**Data:** 25/03/2026 
**Versão:** 1.0

---

## Sinopse

<!-- Três parágrafos máximo. -->
<!-- §1: O problema que o projecto endereça e quem o tem. -->
<!-- §2: A solução proposta e o que a distingue do que já existe. -->
<!-- §3: O resultado esperado e como se verifica que foi atingido. -->
<!-- A sinopse deve ser legível por alguém sem formação técnica. -->

O estudo da teoria musical exige prática. A avaliação é fundamental para a consolidação de conceitos pelo que ferramentas interativas que auxiliem o treino autónomo dos estudantes de música e dos autodidatas são importantes. Tradicionalmente os exercícios são baseados em papel, sem reprodução sonora ou sem possibilidade de correção imediata, o que torna o processo de aprendizagem menos fluido e mais suscetível à perpetuação de erros.

A solução proposta, o "Musical Theory Trainer" será uma plataforma web interativa baseada em geração procedimental para treino da teoria musical. Deve gerar exercícios de identificação de intervalos, escalas e tonalidades, combinando a visualização em notação musical padrão (pauta) com a reprodução sonora do excerto gerado. A avaliação será automática, devolvendo a solução correta e uma breve justificação pedagógica em caso de erro. Como alternativa às formas de aprendizagem tradicionais, existem soluções digitais no mercado. No entanto, a análise de produtos de referência revelou lacunas que o Musical Theory Trainer pode colmatar, ajudando a definir as funcionalidades a incluir e a excluir no projeto. Exemplificando com dois dos grandes players:
•	Musictheory.net: É considerado uma das referências, utilizando uma Single Page Application (SPA) com geração procedimental dinâmica, avaliação imediata e reprodução áudio. No projeto a desenvolver pretende-se colmatar a ausência de gravação de progresso na versão web gratuita do Musictheory (obriga à compra da app móvel Tenuto) através da inclusão de uma base de dados local para garantir a persistência gratuita do histórico do utilizador. Por outro lado, à semelhança do Musictheory, no projeto pretende-se implementar uma arquitetura leve no browser (SPA) e a uma interface limpa e intuitiva.
•	Teoria.com: É também uma das referências que se destaca por disponibilizar exercícios exigentes e muito completos ao nível da teoria musical e treino auditivo, sendo amplamente reconhecido e utilizado no meio académico. Tem uma interface antiquada, pouco responsiva, sendo a curva de aprendizagem demasiado exigente para iniciantes, características que se pretendem evitar no projeto que, à semelhança do Teoria.com, deve ter rigor técnico na validação dos exercícios gerados procedimentalmente, encapsulados num design moderno (HTML5/CSS3) que guia o utilizador através de feedback pedagógico claro quando erra.


O resultado esperado é uma Single Page Application (SPA) funcional, acessível via browser, capaz de disponibilizar variações para os três tipos de exercícios propostos. 
O sucesso do projeto será verificado através da execução fluida do ciclo: geração correta do exercício pelo servidor, apresentação visual e sonora no cliente, processamento da resposta de escolha múltipla e devolução instantânea da solução ao utilizador.


---

## MVP — Definição e critérios de aceitação

<!-- Listar as funcionalidades do núcleo mínimo obrigatório na entrega final. -->
<!-- Para cada funcionalidade, definir um critério de aceitação observável. -->
<!-- Exemplo de critério fraco: "o utilizador consegue autenticar-se" -->
<!-- Exemplo de critério forte: "dado email e password válidos, o sistema autentica e redirige para o dashboard -->
<!--   em menos de 2 segundos; dado email inválido, apresenta mensagem de erro sem expor informação de sistema." -->

### Funcionalidade 1 — Geração e Apresentação de Exercícios 

**Critério de aceitação:**  
Após um clique no botão de "Novo Exercício" (para intervalos, escalas ou tonalidades), o sistema efetua um pedido à API e renderiza uma pauta musical válida no ecrã. Após um clique no botão "Tocar" o sistema reproduz áudio que corresponde às notas desenhadas na pauta.

### Funcionalidade 2 — Sistema de Interação e Resposta 

**Critério de aceitação:**  
Dado um exercício renderizado o sistema apresenta entre 3 botões de escolha múltipla com as hipóteses de resposta. Ao selecionar e clicar numa das opções, os botões ficam bloqueados para evitar respostas dúbias no mesmo exercício.

### Funcionalidade 3 — Avaliação Automática 

**Critério de aceitação:**  
Após submissão da resposta o sistema procede à validação. Se a resposta for correta a interface destaca a opção a verde e apresenta a mensagem "Correto". Se a resposta for incorreta o sistema destaca a opção submetida a vermelho e indica a resposta certa exibindo um parágrafo de texto com a explicação teórica do erro.

### Funcionalidade 4 — Persistência de Resultados 

**Critério de aceitação:**  
Após a avaliação de uma resposta, o sistema grava automaticamente na base de dados o tipo de exercício, a resposta dada (certa/errada) e a data/hora. O utilizador consegue aceder a um painel simples (dashboard) que apresenta a sua taxa de acerto global.

<!-- Adicionar funcionalidades conforme necessário -->

---

## Stack tecnológica

<!-- Para cada tecnologia principal, uma linha de justificação. -->
<!-- Não é necessário ser exaustivo — as decisões menores entram nos ADRs durante o desenvolvimento. -->

| Componente | Tecnologia escolhida | Justificação |
|-----------|---------------------|-------------|
| Frontend | HTML5, CSS3 e JavaScript Vanilla (SPA) | Garante uma navegação fluida sem recarregamentos de página (Single Page Application), ideal para exercícios contínuos |
| Backend | Python com FastAPI | O FastAPI cria uma API REST extremamente rápida sem bloquear o browser |
| Base de dados | SQLite | o SQLite proporciona uma base de dados relacional leve e integrada, ideal para armazenar o histórico de métricas dos alunos sem necessidade de infraestrutura externa complexa |
| Hosting/Deploy | [ex: Railway] | [porquê esta e não outra] |
| Autenticação | [ex: JWT] | [porquê esta e não outra] |

---

## Esboço de arquitectura — C4 Nível 1

<!-- Opcional mas recomendado se já houver clareza sobre a fronteira do sistema. -->
<!-- Pode ser uma imagem, um diagrama em texto, ou uma descrição estruturada. -->
<!-- Vai ser refinado em docs/architecture/c4-context.png durante o desenvolvimento. -->

**Sistema:** Musical Theory Trainer

**Utilizadores:**
- Estudantes de música ou autodidatas —  acedem à aplicação via browser, leem as pautas, ouvem o áudio e submetem as respostas aos exercícios teóricos
- [Tipo de utilizador 2] — [o que fazem com o sistema]

**Sistemas externos:**
- CDNs estáticos para scripts — [como o sistema interage com ele]
- Base de Dados local (SQLite)  — [como o sistema interage com ele]

---

## Calendário individual detalhado

<!-- Adaptar o template do Guia de Projecto ao projecto específico. -->
<!-- As datas das três entregas formais são fixas. O restante é do estudante gerir. -->
<!-- Ser realista: prever tempo para testes, revisão do relatório e preparação da defesa. -->

| Semanas | Datas | Conteúdo planeado | Marco |
|---------|-------|------------------|-------|
| Sem. 1–2 | 17–28 mar | Proposta. Configuração do repositório. | **Proposta (25 mar)** |
| Sem. 3–4 | 31 mar–11 abr | Levantamento de requisitos e desenho da arquitetura (C4 nível 1 e 2). Preparação do repositório GitHub e ambiente de desenvolvimento Python/HTML. | |
| Sem. 5–6 | 14–25 abr | Wireframes da interface gráfica. Início da implementação do núcleo da aplicação (comunicação base entre API REST e a SPA). | |
| Sem. 7 | 28 abr–2 mai | Demo interna. Validação do estado da implementação da arquitetura base. Changelog consolidado, README atualizado. | **Demo interna** |
| Sem. 8 | 5–6 mai | Finalização da documentação. Relatório intercalar: Capítulos 1 (Introdução) e 2 (Desenho) completos. Estado de implementação documentado no Cap. 3.  | **Intercalar (6 mai)** |
| Sem. 9–10 | 7–16 mai | Implementação específica dos três tipos de exercícios: identificação de intervalos, escalas e tonalidades (lógica musical no Backend). Identificação e documentação de limitações. | |
| Sem. 11–12 | 19–30 mai | Implementação completa do MVP. Integração da reprodução de áudio e desenho da notação nas pautas (Frontend). Testes funcionais unitários. Capturas de ecrã e exemplos de execução para Cap. 4. | |
| Sem. 13 | 2–6 jun | Revisão geral, polimento da interface do utilizador e validação dos critérios de aceitação definidos na proposta. Correção de bugs. | |
| Sem. 14 | 9–13 jun | Redação do Capítulo 4 (Testes) e Capítulo 5 (Conclusões). Revisão bibliográfica, formatação APA e preparação dos anexos. | |
| Sem. 15 | 16–20 jun | Reunião de Preparação para a Defesa. Revisão da coerência entre o código desenvolvido e o relatório escrito. Ensaio de perguntas de júri. | **Prep. defesa** |
| Sem. 16 | 24 jun | Afinação final do documento. Código e demo em anexo.  | **Final (24 jun)** |
