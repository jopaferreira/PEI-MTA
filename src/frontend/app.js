// GESTÃO DO INTERFACE E ARRANQUE

// Remove Splash Screen 2 segundos após carregamento da página
window.addEventListener('load', () => {
    const splashScreen = document.getElementById('splash-screen');
    setTimeout(() => {
        splashScreen.classList.add('hidden');
    }, 2000);
});

// VARIÁVEIS GERAIS E CONFIGURAÇÕES
const VF = Vex.Flow; // Atalho para facilitar a chamada da biblioteca VexFlow
const divPauta = document.getElementById("pauta"); // Elemento HTML onde a pauta será desenhada
let melodiaAtual = []; // Variável para guardar temporariamente as notas devolvidas pela API
let synth; // Variável para guardar o sintetizador de áudio (Tone.js)
let exercicioAtual = null; // Guarda os dados completos do exercício a decorrer

// COMUNICAÇÃO COM A API E LÓGICA DE JOGO
// Pede um Novo Exercício ao Python
document.getElementById("btnGerar").addEventListener("click", async () => {
    // Faz um pedido HTTP GET à rota do FastAPI
    const resposta = await fetch("http://127.0.0.1:8000/api/exercicio/novo");
    const dados = await resposta.json();
    
    // Atualiza o estado da aplicação com os dados recebidos
    melodiaAtual = dados.notas;
    exercicioAtual = dados; 
    
    // Atualiza a mensagem de interface
    const status = document.getElementById("status");
    status.innerText = dados.mensagem;
    status.style.color = "#333"; // Reset à cor base do texto
    
    // Desbloqueia o botão de tocar áudio
    document.getElementById("btnTocar").disabled = false;

    // Aciona as funções visuais e dinâmicas
    desenharPauta(melodiaAtual);
    criarBotoesResposta(dados.opcoes, dados.detalhe); // Injeta os botões das opções no ecrã
    atualizarDashboard();
});

// Cria Botões
function criarBotoesResposta(opcoes, respostaCerta) {
    const divOpcoes = document.getElementById("opcoes-resposta");
    divOpcoes.innerHTML = ""; // Limpa os botões do exercício anterior

    // Para cada opção enviada pelo Python, cria um botão HTML
    opcoes.forEach(opcao => {
        const btn = document.createElement("button");
        btn.innerText = opcao;
        btn.className = "btn-warning"; // Aplica o estilo laranja base definido no CSS

        // Avaliação ao clicar numa resposta
        btn.addEventListener("click", async () => {
            const acertou = (opcao === respostaCerta);
            const todosBotoes = divOpcoes.querySelectorAll("button");

            // Feedback Visual imediato através das cores dos botões
            todosBotoes.forEach(b => {
                b.disabled = true; // Bloqueia botões para evitar duplo clique
                if (b.innerText === respostaCerta) {
                    b.style.backgroundColor = "#4CAF50"; // Verde na resposta certa
                } else if (b === btn && !acertou) {
                    b.style.backgroundColor = "#f44336"; // Vermelho na resposta errada
                }
            });

            // Atualiza a mensagem de texto com feedback
            const status = document.getElementById("status");
            if (acertou) {
                status.innerText = "✨ Resposta Correta!";
                status.style.color = "#4CAF50";
            } else {
                status.innerText = `❌ Errado! A resposta certa era: ${respostaCerta}.`;
                status.style.color = "#f44336";
            }

            // Envia o resultado da tentativa para o Python gravar na Base de Dados
            const payload = {
                tipo_exercicio: exercicioAtual.tipo_exercicio,
                detalhe: respostaCerta,
                resposta_dada: opcao,
                correta: acertou
            };

            await fetch("http://127.0.0.1:8000/api/tentativas/", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify(payload)
            });

            atualizarDashboard(); // Pede ao servidor a taxa de acerto atualizada
        });

        divOpcoes.appendChild(btn); // Adiciona o botão à página
    });
}

// Obtém e Atualiza as Métricas para o Dashboard
async function atualizarDashboard() {
    const resposta = await fetch("http://127.0.0.1:8000/api/dashboard/");
    const dados = await resposta.json();
    document.getElementById("dashboard").innerText = 
        `Total Respostas: ${dados.total_tentativas} | Taxa de Acerto: ${dados.taxa_acerto_global}%`;
}


// RENDERIZAÇÃO VISUAL (VEXFLOW) E SONORA (TONE.JS)
// Desenho da Pauta Musical
function desenharPauta(dadosMelodia) {
    divPauta.innerHTML = ""; // Limpa a pauta gráfica anterior do ecrã
    
    // Prepara o "quadro" em formato SVG e define o tamanho
    const renderer = new VF.Renderer(divPauta, VF.Renderer.Backends.SVG);
    renderer.resize(400, 150);
    const context = renderer.getContext();
    
    // Cria as 5 linhas, adiciona a Clave de Sol e o Compasso (4/4)
    const stave = new VF.Stave(10, 0, 350).addClef("treble").addTimeSignature("4/4").setContext(context).draw();

    // Mapeia os dados devolvidos pelo Python para "Notas" gráficas que o VexFlow entende
    const vexNotes = dadosMelodia.map(nota => new VF.StaveNote({ keys: [nota.vexflow], duration: "q" }));
    
    // Agrupa as notas numa "Voz", formata e desenha-as em cima das linhas criadas
    const voice = new VF.Voice({ num_beats: dadosMelodia.length, beat_value: 4 }).addTickables(vexNotes);
    new VF.Formatter().joinVoices([voice]).format([voice], 300);
    voice.draw(context, stave);
}

// Reprodução de Áudio
document.getElementById("btnTocar").addEventListener("click", async () => {
    // O Tone.start() é obrigatório pelas políticas de segurança dos browsers para permitir áudio
    await Tone.start();
    
    // Se o sintetizador ainda não estiver criado, cria-o e liga-o às colunas do computador
    if (!synth) synth = new Tone.Synth().toDestination();
    
    const tempoAtual = Tone.now();
    
    // Percorre cada nota do exercício e toca-a sequencialmente com 0.5s de intervalo
    melodiaAtual.forEach((nota, index) => {
        synth.triggerAttackRelease(nota.tone, "4n", tempoAtual + (index * 0.5));
    });
});