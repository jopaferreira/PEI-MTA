// GESTÃO DA INTERFACE E ARRANQUE

// Remove Splash Screen 2 segundos após carregamento da página e decide qual ecrã mostrar
window.addEventListener('load', () => {
    const splashScreen = document.getElementById('splash-screen');
    if (splashScreen) {
        setTimeout(() => {
            splashScreen.classList.add('hidden');
            // Após o splash, mostra o Login se o não estiver autenticado, ou a App se já tiver sessão
            // Verifica se o utilizador já tem ID (sessão ativa)
            if (localStorage.getItem("userId")) {
                const appScreen = document.getElementById("app-screen");
                if (appScreen) appScreen.style.display = "block";
                atualizarDashboard();
            } else {
                const loginScreen = document.getElementById("login-screen");
                if (loginScreen) loginScreen.style.display = "block";
            }
        }, 2000);
    }
});

// Variáveis Globais
const API_URL = window.location.origin; // Produção (Render) => mesmo domínio
const VF = Vex.Flow;
const divPauta = document.getElementById("pauta");
let melodiaAtual = [];
let synth;
let exercicioAtual = null;
// Para as métricas melhoradas
let sessaoTotal = 0;
let sessaoCertas = 0;
let graficoTiposInstancia = null;
let graficoEvolucaoInstancia = null;
// Variável para indicar se o utilizador não pretende ter conta 
let isGuest = false;
let sessaoTipos = { "Intervalo": [0, 0], "Escala": [0, 0], "Tonalidade": [0, 0] }; // Rastreio local

// AUTENTICAÇÃO
// Função para gerir o login e o registo
async function gerirAutenticacao(rota) {
    const inputUser = document.getElementById("inputUser");
    const inputPass = document.getElementById("inputPass");
    const msgBox = document.getElementById("login-msg");
    // Validação dos campos
    if (!inputUser || !inputPass) return;
    // Verifica se ambos os campos estão preenchidos
    const user = inputUser.value;
    const pass = inputPass.value;
    // Se algum dos campos estiver vazio, mostra mensagem de erro e retorna
    if (!user || !pass) {
        if (msgBox) msgBox.innerText = "Preencha ambos os campos.";
        return;
    }
    // Envia os dados para a API e processa a resposta
    try {
        const resposta = await fetch(`${API_URL}/api/auth/${rota}`, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ username: user, password: pass })
        });

        const dados = await resposta.json();
        // Se a API retornar um erro, mostra a mensagem de erro
        if (dados.status === "erro") {
            if (msgBox) msgBox.innerText = dados.mensagem;
        } else {
            // Sucesso! Grava o ID, esconde o ecrã de login e mostra a aplicação
            localStorage.setItem("userId", dados.id);

            const loginScreen = document.getElementById("login-screen");
            const appScreen = document.getElementById("app-screen");
            // Limpa os campos e mensagens para a próxima vez que o utilizador se autenticar
            if (loginScreen) loginScreen.style.display = "none";
            if (appScreen) appScreen.style.display = "block";
            inputPass.value = "";
            if (msgBox) msgBox.innerText = "";
            // Atualiza o dashboard com os resultados do utilizador
            atualizarDashboard();
        }
    } catch (error) {
        if (msgBox) msgBox.innerText = "Erro de ligação ao servidor.";
    }
}
// Botão de Convidado - acesso sem conta e sem gravação de progresso
const btnConvidado = document.getElementById("btnConvidado");
if (btnConvidado) {
    btnConvidado.addEventListener("click", () => {
        isGuest = true;
        localStorage.removeItem("userId"); // Garante que não há sessão ativa

        document.getElementById("login-screen").style.display = "none";
        document.getElementById("app-screen").style.display = "block";

        // Oculta funcionalidades de utilizador registado
        document.getElementById("bloco-historico").style.display = "none";
        document.getElementById("bloco-evolucao").style.display = "none";
        document.getElementById("bloco-tipos").style.width = "100%"; // Expande o gráfico de sessão

        // Reinicia contadores locais
        sessaoTotal = 0;
        sessaoCertas = 0;
        sessaoTipos = { "Intervalo": [0, 0], "Escala": [0, 0], "Tonalidade": [0, 0] };

        atualizarDashboard();
    });
}

// Verifica se os botões existem antes de adicionar os event listeners para evitar erros em páginas onde eles não estão presentes
const btnEntrar = document.getElementById("btnEntrar");
if (btnEntrar) {
    btnEntrar.addEventListener("click", () => gerirAutenticacao("login"));
}

const btnRegistar = document.getElementById("btnRegistar");
if (btnRegistar) {
    btnRegistar.addEventListener("click", () => gerirAutenticacao("registo"));
}
// Botão de Sair: Limpa a sessão e volta para o ecrã de login
const btnSair = document.getElementById("btnSair");
if (btnSair) {
    btnSair.addEventListener("click", () => {
        localStorage.removeItem("userId");
        const appScreen = document.getElementById("app-screen");
        const loginScreen = document.getElementById("login-screen");
        if (appScreen) appScreen.style.display = "none";
        if (loginScreen) loginScreen.style.display = "block";
    });
    // Repõe interface para o próximo utilizador
    sessaoTotal = 0;
    sessaoCertas = 0;
    isGuest = false;
    document.getElementById("bloco-historico").style.display = "flex";
    document.getElementById("bloco-evolucao").style.display = "block";
    document.getElementById("bloco-tipos").style.width = "45%";
}


// COMUNICAÇÃO COM A API E LÓGICA DE EXERCÍCIOS
const btnGerar = document.getElementById("btnGerar");
if (btnGerar) {
    btnGerar.addEventListener("click", async () => {
        const divOpcoes = document.getElementById("opcoes-resposta");
        const divExplicacao = document.getElementById("explicacao-teorica");
        const filtroExercicio = document.getElementById("filtroExercicio");
        // Limpa a pauta, opções e explicação para o novo exercício
        if (divOpcoes) divOpcoes.innerHTML = "";
        if (divPauta) divPauta.innerHTML = "";
        if (divExplicacao) divExplicacao.style.display = "none";
        // Define o filtro selecionado ou usa "Mistura" como padrão
        const filtroSelecionado = filtroExercicio ? filtroExercicio.value : "Mistura";
        // Solicita um novo exercício com base no filtro selecionado
        try {
            const resposta = await fetch(`${API_URL}/api/exercicio/novo?filtro=${filtroSelecionado}`);
            const dados = await resposta.json();
            // Atualiza as variáveis globais com os dados do exercício recebido
            melodiaAtual = dados.notas || [];
            exercicioAtual = dados;
            // Atualiza o status do exercício e a visibilidade do botão de tocar em função do tipo de exercício
            const status = document.getElementById("status");
            if (status) {
                status.innerText = dados.mensagem;
                status.style.color = "#333";
            }
            // Gestão do Botão Tocar e da Checkbox de Ocultar Pauta
            const btnTocar = document.getElementById("btnTocar");
            const chkOcultarPauta = document.getElementById("chkOcultarPauta");

            if (dados.tipo_exercicio === "Tonalidade") {
                if (btnTocar) btnTocar.style.display = "none";
                // Desativa a opção de ocultar pauta para Tonalidades (precisam do visual)
                if (chkOcultarPauta) {
                    chkOcultarPauta.disabled = true;
                    if (divPauta) divPauta.style.display = "flex"; // Força a visualização
                }
            } else {
                if (btnTocar) {
                    btnTocar.style.display = "inline-block";
                    btnTocar.disabled = false;
                }
                // Reativa a checkbox e aplica a visibilidade escolhida
                if (chkOcultarPauta) {
                    chkOcultarPauta.disabled = false;
                    if (divPauta) divPauta.style.display = chkOcultarPauta.checked ? "none" : "flex";
                }
            }
            // Desenha a pauta com as notas do exercício e cria os botões de resposta
            desenharPauta(dados);
            criarBotoesResposta(dados.opcoes, dados.detalhe);
            atualizarDashboard();
        } catch (e) {
            const status = document.getElementById("status");
            if (status) status.innerText = "Erro ao obter exercício do servidor.";
        }
    });
}


// Cria Botões de Resposta
function criarBotoesResposta(opcoes, respostaCerta) {
    const divOpcoes = document.getElementById("opcoes-resposta");
    if (!divOpcoes) return;

    divOpcoes.innerHTML = "";

    opcoes.forEach(opcao => {
        const btn = document.createElement("button");
        btn.innerText = opcao;
        btn.className = "btn-warning";

        btn.addEventListener("click", async () => {
            const acertou = (opcao === respostaCerta);
            
            const todosBotoes = divOpcoes.querySelectorAll("button");
            // Desativa todos os botões e atribui cores: verde para a resposta certa, vermelho para errada
            todosBotoes.forEach(b => {
                b.disabled = true;
                if (b.innerText === respostaCerta) {
                    b.style.backgroundColor = "#4CAF50";
                } else if (b === btn && !acertou) {
                    b.style.backgroundColor = "#f44336";
                }
            });
            
            // Atualiza o status da resposta e mostra a explicação
            const status = document.getElementById("status");
            const divExplicacao = document.getElementById("explicacao-teorica");
            
            if (acertou) {
                if (status) {
                    status.innerText = "✨ Resposta Correta!";
                    status.style.color = "#4CAF50";
                }
            } else {
                if (status) {
                    status.innerText = `❌ Errado! A resposta certa era: ${respostaCerta}.`;
                    status.style.color = "#f44336";
                }
                if (divExplicacao && exercicioAtual) {
                    divExplicacao.innerHTML = `<strong>Dica de Estudo:</strong> ${exercicioAtual.explicacao}`;
                    divExplicacao.style.display = "block";
                }
            }
            
            // Registo de métricas e gravação na BD
            if (exercicioAtual) {
                // Incrementa as variáveis da sessão (Modo Registado e Convidado)
                sessaoTotal++;
                if (acertou) sessaoCertas++;

                // Rastreio local por tipo de exercício
                sessaoTipos[exercicioAtual.tipo_exercicio][1]++;
                if (acertou) sessaoTipos[exercicioAtual.tipo_exercicio][0]++;

                // Só envia para a Base de Dados se NÃO for convidado (isGuest = false)
                if (!isGuest) {
                    const userId = localStorage.getItem("userId");
                    if (userId) {
                        try {
                            await fetch(`${API_URL}/api/tentativas`, {
                                method: "POST",
                                headers: { "Content-Type": "application/json" },
                                body: JSON.stringify({
                                    utilizador_id: parseInt(userId),
                                    tipo_exercicio: exercicioAtual.tipo_exercicio,
                                    correta: acertou
                                })
                            });
                        } catch (e) {
                            console.error("Erro ao guardar tentativa.");
                        }
                    }
                }

                // Atualiza os gráficos sempre (quer seja convidado ou não)
                atualizarDashboard();
            }
        });

        divOpcoes.appendChild(btn);
    });
}


// Obtém e atualiza os resultados no Dashboard e Gráficos
async function atualizarDashboard() {
    // Atualiza o texto da Sessão Atual
    const statSessao = document.getElementById("stat-sessao");
    const taxaSessao = sessaoTotal > 0 ? ((sessaoCertas / sessaoTotal) * 100).toFixed(1) : 0;
    if (statSessao) statSessao.innerText = `${sessaoCertas} / ${sessaoTotal} (${taxaSessao}%)`;

    if (graficoTiposInstancia) graficoTiposInstancia.destroy();
    const ctxTipos = document.getElementById('graficoTipos').getContext('2d');

    // utilizadores sem registo
    if (isGuest) {
        const dadosLocais = {};
        for (const [tipo, valores] of Object.entries(sessaoTipos)) {
            dadosLocais[tipo] = valores[1] > 0 ? ((valores[0] / valores[1]) * 100).toFixed(1) : 0;
        }

        graficoTiposInstancia = new Chart(ctxTipos, {
            type: 'bar',
            data: {
                labels: Object.keys(dadosLocais),
                datasets: [{
                    label: '% de Acerto (Sessão Atual)',
                    data: Object.values(dadosLocais),
                    backgroundColor: ['#4CAF50', '#008CBA', '#f0ad4e'],
                    borderRadius: 5
                }]
            },
            options: { responsive: true, maintainAspectRatio: false, scales: { y: { beginAtZero: true, max: 100 } }, plugins: { title: { display: true, text: 'Desempenho por Tópico (Sessão)' }, legend: { display: false } } }
        });
        return; 
    }

    // utilizadores Registados 
    const userId = localStorage.getItem("userId");
    if (!userId) return;

    try {
        const resposta = await fetch(`${API_URL}/api/dashboard/${userId}`);
        const dados = await resposta.json();

        // Atualiza texto Global
        const statGlobal = document.getElementById("stat-global");
        if (statGlobal) statGlobal.innerText = `${dados.total} exercícios (${dados.taxa_global}%)`;

        // Elimina gráficos antigos antes de redesenhar para evitar sobreposição
        if (graficoEvolucaoInstancia) graficoEvolucaoInstancia.destroy();

        // Gráfico de Barras: Taxa desagregada por tipo de exercício
        graficoTiposInstancia = new Chart(ctxTipos, {
            type: 'bar',
            data: {
                labels: Object.keys(dados.por_tipo),
                datasets: [{
                    label: '% de Acerto',
                    data: Object.values(dados.por_tipo),
                    backgroundColor: ['#4CAF50', '#008CBA', '#f0ad4e'],
                    borderRadius: 5
                }]
            },
            options: {
                responsive: true, maintainAspectRatio: false,
                scales: { y: { beginAtZero: true, max: 100 } },
                plugins: {
                    title: { display: true, text: 'Desempenho por Tópico' },
                    legend: { display: false }
                }
            }
        });

        // Gráfico de Linhas: Evolução Diária vs Acumulada
        const ctxEvolucao = document.getElementById('graficoEvolucao').getContext('2d');
        const datas = dados.evolucao_diaria.map(d => d.data);
        const taxasDia = dados.evolucao_diaria.map(d => d.taxa_dia);
        const taxasAcum = dados.evolucao_diaria.map(d => d.taxa_acumulada);

        graficoEvolucaoInstancia = new Chart(ctxEvolucao, {
            type: 'line',
            data: {
                labels: datas.length > 0 ? datas : ['Hoje'],
                datasets: [
                    {
                        label: 'Média do Dia (%)',
                        data: taxasDia.length > 0 ? taxasDia : [0],
                        borderColor: '#64748b',
                        borderDash: [5, 5], 
                        tension: 0.3,
                        fill: false
                    },
                    {
                        label: 'Acumulada Histórica (%)',
                        data: taxasAcum.length > 0 ? taxasAcum : [0],
                        borderColor: '#4361ee',
                        borderWidth: 3,
                        tension: 0.3,
                        fill: true,
                        backgroundColor: 'rgba(67, 97, 238, 0.1)'
                    }
                ]
            },
            options: {
                responsive: true, maintainAspectRatio: false,
                scales: { y: { beginAtZero: true, max: 100 } },
                plugins: {
                    title: { display: true, text: 'Progresso ao longo do tempo' }
                }
            }
        });

    } catch (e) {
        console.error("Erro ao carregar métricas analíticas.");
    }
}

// Configuração do Hard Reset
const btnReset = document.getElementById("btnReset");
if (btnReset) {
    btnReset.addEventListener("click", async () => {
        if (confirm("Tem a certeza que deseja apagar todo o seu histórico? Esta ação é irreversível.")) {
            const userId = localStorage.getItem("userId");
            try {
                await fetch(`${API_URL}/api/usuarios/${userId}/reset`, { method: "DELETE" });
                sessaoTotal = 0;
                sessaoCertas = 0;
                atualizarDashboard();
            } catch (e) {
                console.error("Erro ao reiniciar dados.");
            }
        }
    });
}


// Desenho da Pauta Musical (VexFlow)
function desenharPauta(dados) {
    if (!divPauta) return;
    divPauta.innerHTML = "";
    // Define a largura da pauta com base no número de notas: mais notas exigem uma pauta mais longa
    const larguraPauta = (dados.notas && dados.notas.length > 2) ? 550 : 250;
    // Cria o renderer do VexFlow e a pauta, adicionando a clave de sol e, se for um exercício de tonalidade, a armação de clave correspondente
    const renderer = new VF.Renderer(divPauta, VF.Renderer.Backends.SVG);
    renderer.resize(larguraPauta + 50, 150);
    const context = renderer.getContext();
    const stave = new VF.Stave(10, 0, larguraPauta).addClef("treble");
    // Para exercícios de tonalidade, em vez de desenhar notas, desenha a armação de clave correspondente ao número de acidentes 
    if (dados.tipo_exercicio === "Tonalidade") {
        // Atribui número de acidentes para a armação de clave 
        const vexflowKeys = {
            "-7": "Cb", "-6": "Gb", "-5": "Db", "-4": "Ab", "-3": "Eb", "-2": "Bb", "-1": "F",
            "0": "C",
            "1": "G", "2": "D", "3": "A", "4": "E", "5": "B", "6": "F#", "7": "C#"
        };
        const chave = vexflowKeys[dados.num_acidentes.toString()];
        stave.addKeySignature(chave);
        stave.setContext(context).draw();
        return;
    }
    // Para exercícios de leitura de notas, desenha a pauta com as notas fornecidas pela API
    stave.addTimeSignature("4/4").setContext(context).draw();
    // Converte as notas do formato da API para o formato do VexFlow, adicionando acidentes quando necessário
    const vexNotes = dados.notas.map(nota => {
        const staveNote = new VF.StaveNote({ keys: [nota.vexflow], duration: "q" });
        let sinal = null;
        if (nota.vexflow.includes("#")) {
            sinal = new VF.Accidental("#");
        } else if (nota.vexflow.charAt(1) === "b") {
            sinal = new VF.Accidental("b");
        }

        if (sinal) {
            try { staveNote.addModifier(sinal, 0); } catch (e) { staveNote.addModifier(0, sinal); }
        }
        return staveNote;
    });

    const voice = new VF.Voice({ num_beats: dados.notas.length, beat_value: 4 }).addTickables(vexNotes);
    new VF.Formatter().joinVoices([voice]).format([voice], larguraPauta - 50);
    voice.draw(context, stave);
}


// Reprodução de Áudio (Tone.js) com seleção de timbre
const btnTocar = document.getElementById("btnTocar");
if (btnTocar) {
    btnTocar.addEventListener("click", async () => {
        if (melodiaAtual.length === 0) return;
        await Tone.start();
        
        const seletorTimbre = document.getElementById("seletorTimbre");
        const tipoTimbre = seletorTimbre ? seletorTimbre.value : "Synth";

        // Limpa o sintetizador anterior para evitar sobreposição
        if (synth) {
            synth.dispose();
        }

        // Novo sintetizador com base na escolha do utilizador para o timbre 
        if (tipoTimbre === "FMSynth") {
            synth = new Tone.FMSynth().toDestination();
        } else if (tipoTimbre === "AMSynth") {
            synth = new Tone.AMSynth().toDestination();
        } else if (tipoTimbre === "PluckSynth") {
            synth = new Tone.PluckSynth().toDestination();
        } else {
            // Lida automaticamente com: "sine", "triangle", "square" e "sawtooth"
            synth = new Tone.Synth({ oscillator: { type: tipoTimbre } }).toDestination();
        }

        const tempoAtual = Tone.now();
        melodiaAtual.forEach((nota, index) => {
            synth.triggerAttackRelease(nota.tone, "4n", tempoAtual + (index * 0.5));
        });
    });
}

// Ocultar/Mostrar Pauta (Treino Auditivo)
const chkOcultarPauta = document.getElementById("chkOcultarPauta");
if (chkOcultarPauta && divPauta) {
    chkOcultarPauta.addEventListener("change", (e) => {
        // Bloqueia a ação se for um exercício de Tonalidade
        if (exercicioAtual && exercicioAtual.tipo_exercicio === "Tonalidade") {
            divPauta.style.display = "flex";
            return;
        }
        // Alterna entre display 'none' (escondido) e 'flex' 
        divPauta.style.display = e.target.checked ? "none" : "flex";
    });
}