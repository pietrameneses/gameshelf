// chave RAWG API 
let RAWG_KEY = ""

// jogo selecionado
let jogoAtual = null

// busca a key do servidor
fetch("/config")
    .then(res => res.json())
    .then(data => {
        RAWG_KEY = data.rawg_key
        carregarShelf() 
    })

// busca
function buscarJogo() {
    const query = document.getElementById("inputBusca").value
    if (!query) return
 
    fetch(`https://api.rawg.io/api/games?key=${RAWG_KEY}&search=${query}`)
        .then(res => res.json())
        .then(data => mostrarResultados(data.results))
}

// busca com enter
document.addEventListener("DOMContentLoaded", () => {
    document.getElementById("inputBusca").addEventListener("keypress", e => {
        if (e.key === "Enter") buscarJogo()
    })
})

// results da busca
function mostrarResultados(jogos) {
    const div = document.getElementById("resultadosBusca")
    div.innerHTML = ""  // limpa resultados anteriores

    jogos.forEach(jogo => {
        const plataformas = jogo.platforms
            ? jogo.platforms.map(p => p.platform.name).join(", ")
            : "N/A"

        div.innerHTML += `
            <div class="col-md-3 mb-4">
                <div class="game-card" onclick="abrirModal(${jogo.id}, '${jogo.name.replace(/'/g, "")}', '${jogo.background_image}', '${plataformas.replace(/'/g, "")}')">
                    <img src="${jogo.background_image || '/static/placeholder.jpg'}" alt="${jogo.name}">
                    <div class="card-body">
                        <div class="card-title">${jogo.name}</div>
                        <div class="card-text">${plataformas}</div>
                    </div>
                </div>
            </div>
        `
    })
}

// modal
function abrirModal(id, nome, imagem, plataformas) {
    jogoAtual = { id, nome, imagem, plataformas }
 
    document.getElementById("modalNome").innerText = nome
    document.getElementById("modalImagem").src = imagem
    document.getElementById("modalPlataformas").innerText = "Plataformas: " + plataformas
    document.getElementById("modalNota").value = ""
    document.getElementById("modalHoras").value = ""
    document.getElementById("modalReview").value = ""
    document.getElementById("modalStatus").value = "quero_jogar"
 
    // verifica se o jogo já está na shelf
    fetch("/jogos")
        .then(res => res.json())
        .then(jogos => {
            const encontrado = jogos.find(j => j.id === id)
            if (encontrado) {
                document.getElementById("modalStatus").value = encontrado.status || "quero_jogar"
                document.getElementById("modalNota").value = encontrado.nota || ""
                document.getElementById("modalHoras").value = encontrado.horas || ""
                document.getElementById("modalReview").value = encontrado.review || ""
            }
        })
 
    const modal = new bootstrap.Modal(document.getElementById("modalJogo"))
    modal.show()
}

// salvar
function salvarJogo() {
    if (!jogoAtual) return
 
    const status = document.getElementById("modalStatus").value
    const nota = parseInt(document.getElementById("modalNota").value) || null
    const horas = parseInt(document.getElementById("modalHoras").value) || 0
    const review = document.getElementById("modalReview").value
 
    // tenta adicionar primeiro
    fetch("/jogos", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
            game_id: jogoAtual.id,
            nome: jogoAtual.nome,
            status: status,
            plataforma: jogoAtual.plataformas
        })
    })
    .then(res => res.json())
    .then(() => {
        // depois atualiza com nota, horas e review
        return fetch(`/jogos/${jogoAtual.id}`, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ nota, horas, review, status })
        })
    })
    .then(() => {
        bootstrap.Modal.getInstance(document.getElementById("modalJogo")).hide()
        carregarShelf()
    })
}

// remover
function removerJogo() {
    if (!jogoAtual) return
 
    fetch(`/jogos/${jogoAtual.id}`, { method: "DELETE" })
        .then(() => {
            bootstrap.Modal.getInstance(document.getElementById("modalJogo")).hide()
            carregarShelf()
        })
}

let statusAtual = "quero_jogar"
 
function filtrarShelf(status) {
    statusAtual = status
 
    // atualiza aba ativa
    document.querySelectorAll(".nav-link").forEach(a => a.classList.remove("active"))
    event.target.classList.add("active")
 
    carregarShelf()
}
 
// carrega shelf
function carregarShelf() {
    fetch(`/jogos?status=${statusAtual}`)
        .then(res => res.json())
        .then(jogos => mostrarShelf(jogos))
}
 
function mostrarShelf(jogos) {
    const div = document.getElementById("shelf")
    div.innerHTML = ""
 
    if (jogos.length === 0) {
        div.innerHTML = `<p class="text-muted mt-3">Nenhum jogo aqui ainda.</p>`
        return
    }
 
    jogos.forEach(jogo => {
        div.innerHTML += `
            <div class="col-md-3 mb-4">
                <div class="game-card" onclick="abrirModal(${jogo.id}, '${jogo.nome.replace(/'/g, "")}', '${jogo.imagem || ""}', '${(jogo.plataforma || "").replace(/'/g, "")}')">
                    <img src="${jogo.imagem || ''}" alt="${jogo.nome}">
                    <div class="card-body">
                        <div class="card-title">${jogo.nome}</div>
                        <div class="card-text">
                            ${jogo.nota ? `<span class="nota-badge">⭐ ${jogo.nota}/5</span>` : ""}
                            <span class="ms-2">${jogo.plataforma || ""}</span>
                        </div>
                    </div>
                </div>
            </div>
        `
    })
}
 