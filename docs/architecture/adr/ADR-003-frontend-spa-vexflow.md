# ADR-003 — Arquitetura SPA com VexFlow e Tone.js

**Data:** 12 de abril de 2026
**Estado:** Aceite
**Decisores:** João Paulo Ramos Ferreira

---

## Contexto

A aplicação precisa de desenhar pautas musicais com exatidão e reproduzir o som das notas geradas, de forma dinâmica. A interação deve ser imediata (informa sobre resposta certa/errada), sem que a página recarregue.

---

## Decisão

Decidi construir uma **Single Page Application (SPA)** em HTML/CSS/JS nativo, incorporando as bibliotecas **VexFlow** (visualização) e **Tone.js** (sintetização de áudio).

---

## Alternativas consideradas

| Alternativa | Razão de rejeição |
|------------|------------------|
| Aplicação Nativa (Mobile iOS/Android) | Foge ao âmbito estipulado para o MVP e limitaria o acesso universal via browser. |
| Imagens e Áudio Estáticos (PNG/MP3) | Incompatível com o requisito "geração procedimental". Obriga a ter um servidor a alojar ficheiros estáticos para cobrir as combinações musicais possíveis. |

---

## Consequências

**Positivas:**
- O processamento visual e sonoro é transferido para o dispositivo do utilizador (cliente), libertando o servidor Backend de carga excessiva.
- O VexFlow gera ficheiros vetoriais (SVG), garantindo que as pautas não perdem qualidade em função do ecrã.

**Negativas / trade-offs:**
- Exige o controlo do estado da página via JavaScript (ex: ecrã de carregamento obrigatório enquanto os scripts não estão prontos).
- Obriga a interação manual do utilizador (clicar no botão) para contornar as políticas restritas de autoplay de áudio dos browsers modernos.