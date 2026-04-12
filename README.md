# 🎮 GameShelf

> Organize, avalie e descubra jogos em um só lugar.

![CI](https://github.com/SEU_USUARIO/gameshelf/actions/workflows/ci.yml/badge.svg)

---

## Sobre o Projeto

GameShelf é uma aplicação web local que resolve um problema comum entre jogadores: a dificuldade de organizar e acompanhar os jogos que jogou, está jogando ou quer jogar. Inspirado em plataformas como Letterboxd e Fragrantica, o GameShelf permite criar listas personalizadas, avaliar jogos, escrever reviews e descobrir títulos similares — tudo integrado com a RAWG API.

---

## Público-alvo

Jogadores casuais e entusiastas que querem manter um registro pessoal da sua jornada nos games.

---

## Funcionalidades

- Busca de jogos via RAWG API (com capa, plataformas e informações)
- Listas personalizáveis ("Quero Jogar", "Jogando", "Zerado" + listas próprias)
- Avaliação com nota de 1 a 5
- Reviews pessoais por jogo
- Registro de horas jogadas
- Adição de um jogo em múltiplas listas simultaneamente
- Remoção de jogos e listas personalizadas
- Dados salvos localmente em JSON

---

## Tecnologias

| Camada | Tecnologia |
|---|---|
| Backend | Python 3 + Flask |
| Frontend | HTML + CSS + JavaScript |
| Estilo | Bootstrap 5 |
| Dados | JSON local |
| API externa | RAWG API |
| Testes | pytest |
| Linting | ruff |
| CI | GitHub Actions |

---

## Estrutura do Projeto

```
gameshelf/
├── src/
│   ├── app.py          # servidor Flask e rotas
│   ├── shelf.py        # lógica de negócio
│   └── data/
│       └── shelf.json  # dados salvos localmente
├── static/
│   ├── style.css
│   └── script.js
├── templates/
│   └── index.html
├── tests/
│   └── test_shelf.py
├── .github/
│   └── workflows/
│       └── ci.yml
├── requirements.txt
├── .gitignore
└── README.md
```

---

## Instalação

**Pré-requisitos:** Python 3.10+, Git

```bash
# clone o repositório
git clone https://github.com/SEU_USUARIO/gameshelf.git
cd gameshelf

# instale as dependências
pip install -r requirements.txt
```

---

## Configuração da API

Crie um arquivo `.env` na raiz do projeto:

```
RAWG_KEY=sua_chave_aqui
```

Obtenha sua chave gratuita em [rawg.io/apidocs](https://rawg.io/apidocs).

---

## Como Executar

```bash
python3 src/app.py
```

Acesse no navegador: [http://localhost:5000](http://localhost:5000)

---

## Como Rodar os Testes

```bash
python3 -m pytest tests/ -v
```

---

## Como Rodar o Linting

```bash
ruff check src/
```

---

## Versão

`1.0.0`

---

## Licença

MIT

## Autor

Pietra Meneses

## Repositório

https://github.com/pietrameneses/gameshelf
