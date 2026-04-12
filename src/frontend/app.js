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


// COMUNICAÇÃO COM A API (BACKEND)
// Pede um Novo Exercício ao Python
document.getElementById("btnGerar").addEventListener("click", async () => {
    // Faz um pedido HTTP GET à rota do FastAPI
    const resposta = await fetch("http://127.0.0.1:8000/api/exercicio/novo");
    const dados = await resposta.json();
    
    // Atualiza o estado da aplicação com os dados recebidos
    melodiaAtual = dados.notas;
    document.getElementById("status").innerText = dados.mensagem;
    
    // Desbloqueia os botões de ação
    document.getElementById("btnTocar").disabled = false;
    document.getElementById("btnResponder").disabled = false;

    // Aciona as funções visuais e de métricas
    desenharPauta(melodiaAtual);
    atualizarDashboard();
});

// Grava a resposta na Base de Dados
document.getElementById("btnResponder").addEventListener("click", async () => {
    // Cria a estrutura exigida pelo Backend
    const payload = {
        tipo_exercicio: "Escala",
        detalhe: "Escala Maior",
        resposta_dada: "Opção Correta",
        correta: true
    };

    // Pedido HTTP POST e envia a resposta em formato JSON
    await fetch("http://127.0.0.1:8000/api/tentativas/", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(payload)
    });

    // Atualiza a interface gráfica e bloqueia o botão para evitar respostas duplicadas
    document.getElementById("status").innerText = "Resposta gravada com sucesso!";
    document.getElementById("btnResponder").disabled = true;
    atualizarDashboard(); // Recalcula a percentagem após esta nova resposta
});

// Obtém e Atualiza as Métricas para o Dashboard
async function atualizarDashboard() {
    // Obtém os resultados do cálculo e exibe no ecrã
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
    
    // Se o sintetizador ainda não estiver criado, cria-oe liga-o às colunas do computador
    if (!synth) synth = new Tone.Synth().toDestination();
    
    const tempoAtual = Tone.now();
    
    // Percorre cada nota do exercício e toca-a sequencialmente com 0.5s de intervalo
    melodiaAtual.forEach((nota, index) => {
        synth.triggerAttackRelease(nota.tone, "4n", tempoAtual + (index * 0.5));
    });
});