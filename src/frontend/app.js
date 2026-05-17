// GESTÃO DA INTERFACE E ARRANQUE

// Remove Splash Screen 2 segundos após carregamento da página
window.addEventListener('load', () => {
    const splashScreen = document.getElementById('splash-screen');
    setTimeout(() => {
        splashScreen.classList.add('hidden');
    }, 2000);
});

// VARIÁVEIS GERAIS E CONFIGURAÇÕES
const API_URL = (window.location.port === "5500")
    ? "http://127.0.0.1:8000"   // Live Server → aponta para o backend local
    : window.location.origin;    // Produção (Render) → mesmo domínio
const VF = Vex.Flow; // Atalho para facilitar a chamada da biblioteca VexFlow
const divPauta = document.getElementById("pauta"); // Elemento HTML onde a pauta será desenhada
let melodiaAtual = []; // Variável para guardar temporariamente as notas devolvidas pela API
let synth; // Variável para guardar o sintetizador de áudio (Tone.js)
let exercicioAtual = null; // Guarda os dados completos do exercício a decorrer

// COMUNICAÇÃO COM A API E LÓGICA DE JOGO
// Pede um Novo Exercício ao Python
document.getElementById("btnGerar").addEventListener("click", async () => {
    // Limpa a interface
    document.getElementById("opcoes-resposta").innerHTML = "";
    divPauta.innerHTML = "";
    document.getElementById("explicacao-teorica").style.display = "none";
    // Lê qual o modo de treino escolhido pelo utilizador na caixa de seleção
    const filtroSelecionado = document.getElementById("filtroExercicio").value;

    // Pede ao Python, enviando o filtro na URL (ex: /api/exercicio/novo?filtro=Escala)
    const resposta = await fetch(`${API_URL}/api/exercicio/novo?filtro=${filtroSelecionado}`);
    const dados = await resposta.json();
    
    // Proteção: para as tonalidades, a lista de notas vem vazia
    melodiaAtual = dados.notas || []; 
    exercicioAtual = dados; 
    
    const status = document.getElementById("status");
    status.innerText = dados.mensagem;
    status.style.color = "#333"; 
    
    // Lógica para o botão "Tocar" (ocultar nas Tonalidades)
    const btnTocar = document.getElementById("btnTocar");
    if (dados.tipo_exercicio === "Tonalidade") {
        btnTocar.style.display = "none";
    } else {
        btnTocar.style.display = "inline-block";
        btnTocar.disabled = false;
    }

    // Passa o objeto 'dados' completo em vez de apenas as notas
    desenharPauta(dados); 
    criarBotoesResposta(dados.opcoes, dados.detalhe); 
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

        // Avaliação e gravação da resposta
        btn.addEventListener("click", async () => {
            const acertou = (opcao === respostaCerta);
            const todosBotoes = divOpcoes.querySelectorAll("button");

            // Sinalização visual do resultado através das cores dos botões
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
            // Seleciona a caixa de feedback pedagógico
            const divExplicacao = document.getElementById("explicacao-teorica"); 

            if (acertou) {
                status.innerText = "✨ Resposta Correta!";
                status.style.color = "#4CAF50";
            } else {
                status.innerText = `❌ Errado! A resposta certa era: ${respostaCerta}.`;
                status.style.color = "#f44336";
                
                // Mostra a justificação teórica
                divExplicacao.innerHTML = `<strong>Dica de Estudo:</strong> ${exercicioAtual.explicacao}`;
                divExplicacao.style.display = "block";
            }

            // Envia o resultado da tentativa para o Python gravar na Base de Dados
            const payload = {
                tipo_exercicio: exercicioAtual.tipo_exercicio,
                detalhe: respostaCerta,
                resposta_dada: opcao,
                correta: acertou
            };

            await fetch(`${API_URL}/api/tentativas/`, {
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
    const resposta = await fetch(`${API_URL}/api/dashboard/`);
    const dados = await resposta.json();
    document.getElementById("dashboard").innerText = 
        `Total Respostas: ${dados.total_tentativas} | Taxa de Acerto: ${dados.taxa_acerto_global}%`;
}


// RENDERIZAÇÃO VISUAL (VEXFLOW) E SONORA (TONE.JS)
// Desenho da Pauta Musical
function desenharPauta(dados) {
    divPauta.innerHTML = ""; 
    
    // Largura aumentada para 550px para caberem os acidentes
    const larguraPauta = (dados.notas && dados.notas.length > 2) ? 550 : 250;
    
    const renderer = new VF.Renderer(divPauta, VF.Renderer.Backends.SVG);
    renderer.resize(larguraPauta + 50, 150);
    const context = renderer.getContext();
    
    const stave = new VF.Stave(10, 0, larguraPauta).addClef("treble");

    // Se for Tonalidade, desenha apenas a armação de clave
    if (dados.tipo_exercicio === "Tonalidade") {
        // Dicionário para converter o número de acidentes nas "Keys" do VexFlow
        const vexflowKeys = {
            "-7": "Cb", "-6": "Gb", "-5": "Db", "-4": "Ab", "-3": "Eb", "-2": "Bb", "-1": "F",
            "0": "C", 
            "1": "G", "2": "D", "3": "A", "4": "E", "5": "B", "6": "F#", "7": "C#"
        };
        
        const chave = vexflowKeys[dados.num_acidentes.toString()];
        
        // Adiciona a armação de clave correta à pauta
        stave.addKeySignature(chave);
        stave.setContext(context).draw();
        
        // Sai da função imediatamente pois não há notas para desenhar
        return; 
    }

    // Para Intervalos e Escalas desenhamos as notas
    stave.addTimeSignature("4/4").setContext(context).draw();

    const vexNotes = dados.notas.map(nota => {
        const staveNote = new VF.StaveNote({ keys: [nota.vexflow], duration: "q" });
        
        // Verifica qual o acidente necessário
        let sinal = null;
        if (nota.vexflow.includes("#")) {
            sinal = new VF.Accidental("#");
        } else if (nota.vexflow.charAt(1) === "b") { 
            sinal = new VF.Accidental("b");
        }
        
        // Aplica o acidente - suporta VexFlow antigo e moderno
        if (sinal) {
            try {
                staveNote.addModifier(sinal, 0); 
            } catch (e) {
                staveNote.addModifier(0, sinal); 
            }
        }
        
        return staveNote;
    });
    
    const voice = new VF.Voice({ num_beats: dados.notas.length, beat_value: 4 }).addTickables(vexNotes);
    
    new VF.Formatter().joinVoices([voice]).format([voice], larguraPauta - 50);
    voice.draw(context, stave);
}

// Reprodução de Áudio
document.getElementById("btnTocar").addEventListener("click", async () => {
    // Se o array de notas estiver vazio não avançar
    if (melodiaAtual.length === 0) return;

    // O Tone.start() é obrigatório pelas políticas de segurança dos browsers para permitir áudio
    await Tone.start();
    
    // Se o sintetizador ainda não estiver criado, cria-o e liga-o
    if (!synth) synth = new Tone.Synth().toDestination();
    
    const tempoAtual = Tone.now();
    
    // Percorre cada nota do exercício e toca-a sequencialmente com 0.5s de intervalo
    melodiaAtual.forEach((nota, index) => {
        synth.triggerAttackRelease(nota.tone, "4n", tempoAtual + (index * 0.5));
    });
});