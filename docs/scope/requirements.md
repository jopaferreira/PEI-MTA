# Levantamento de Requisitos

**Projecto:** Musical Theory Trainer com Geração Procedimental e Avaliação Automática 
**Versão:** 1.0 · 12 de abril de 2026  
**Referência MoSCoW:** https://www.productplan.com/glossary/moscow-prioritization/

---

## Método MoSCoW

| Categoria | Significado |
|-----------|------------|
| **Must have** | Obrigatório. Sem isto o projecto não é entregável. |
| **Should have** | Importante mas não crítico. Incluir se o tempo permitir. |
| **Could have** | Desejável. Só se tudo o resto estiver concluído. |
| **Won't have** | Explicitamente fora do âmbito desta versão. |

---

## Requisitos funcionais

<!-- O que o sistema faz. -->

### Must have

- RF01 — O sistema deve gerar aleatoriamente exercícios musicais de identificação de intervalos, escalas e tonalidades.
- RF02 — O sistema deve renderizar visualmente a pauta correspondente ao exercício gerado utilizando notação musical padrão.
- RF03 — O sistema deve reproduzir o áudio exato das notas desenhadas na pauta.
- RF04 — O sistema deve apresentar opções de resposta em formato de escolha múltipla (mínimo de 3 opções).
- RF05 — O sistema deve bloquear os botões de resposta após a submissão para evitar múltiplas tentativas no mesmo exercício.
- RF06 — O sistema deve avaliar a resposta e apresentar *feedback* visual imediato (destaque a verde para correto, vermelho para incorreto).
- RF07 — Em caso de erro, o sistema deve apresentar a resposta certa acompanhada de uma justificação pedagógica.
- RF08 — O sistema deve persistir automaticamente os resultados na base de dados local (tipo de exercício, resposta dada, correção e data/hora).
- RF09 — O sistema deve disponibilizar um *dashboard* com o total de exercícios realizados e a taxa de acerto global do utilizador.

### Should have

- RF10 — Autenticação básica de utilizadores, permitindo perfis distintos no mesmo dispositivo local.
- RF11 — Filtros no *dashboard* para visualização da taxa de acerto detalhada por categoria de exercício.

### Could have

- RF12 — Suporte para atalhos de teclado (ex: teclas 1, 2 e 3 para submeter opções de resposta).
- RF13 — Sistema básico de gamificação (ex: selos de conquista por séries de respostas certas consecutivas).

### Won't have (nesta versão)

- RF14 — Integração de *hardware* externo (suporte para teclados físicos MIDI).
- RF15 — Aplicação móvel nativa para iOS ou Android.
- RF16 — Painel de administração para gestão de turmas e visualização de notas por professores.

---

## Requisitos não-funcionais

<!-- Como o sistema se comporta: performance, segurança, usabilidade, escalabilidade. -->

### Must have

- RNF01 — **Performance:** A renderização da pauta visual e o carregamento do excerto de áudio devem ocorrer em menos de 1 segundo após o pedido à API.
- RNF02 — **Usabilidade:** A interface gráfica deve ser suficientemente limpa e intuitiva para que um utilizador iniciante consiga realizar um exercício sem necessidade de ler documentação ou tutoriais.
- RNF03 — **Compatibilidade:** O sistema deve ser totalmente funcional nos *browsers* web modernos (Chrome, Firefox, Edge, Safari).

### Should have

- RNF04 — **Manutenibilidade:** A arquitetura deve respeitar o princípio de *Separation of Concerns* (separação clara entre API Backend e SPA Frontend) para facilitar futuras atualizações.

### Could have

- RNF05 — **Acessibilidade:** Suporte a modo de alto contraste para facilitar a leitura das pautas e do texto explicativo.

---

## Histórico de alterações

| Versão | Data | Alteração | Razão |
|--------|------|-----------|-------|
| 1.0 | 04/04/2026 | Versão inicial completa | Levantamento de requisitos para o MVP |

