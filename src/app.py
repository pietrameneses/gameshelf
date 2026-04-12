import os
from dotenv import load_dotenv

# importa o flask
from flask import Flask, request, jsonify, render_template     
# importa o arq. shelf.py
from shelf import add_game, get_games, update_game, remove_game, add_list, get_lists, remove_list

load_dotenv()

# cria o app
app = Flask(__name__, template_folder="../templates", static_folder="../static")

# rota p user acessar a pag inicial e servir o html
@app.route("/")
def home():
    return render_template("index.html")

# rota p pedir a lista de jogos p server + fitros opcionais
@app.route("/jogos", methods=["GET"])
def listar_jogos():
    status = request.args.get("status")
    plataforma = request.args.get("plataforma")
    jogos = get_games(status=status, plataforma=plataforma)
    return jsonify(jogos)

# rota p add jogo
@app.route("/jogos", methods=["POST"])
def add_jogo():
    dados = request.get_json()
    resultado = add_game(dados["game_id"], dados["nome"], dados["status"], dados["plataforma"],  dados.get("imagem", ""))
    return jsonify(resultado)

# rota p atualizar jogos
@app.route("/jogos/<int:game_id>", methods=["POST"])
def atualizar_jogo(game_id):
    dados = request.get_json()
    resultado = update_game(
    game_id,
    nota=dados.get("nota"),
    review=dados.get("review"),
    status=dados.get("status"),
    horas=dados.get("horas"),
    tags=dados.get("tags")
    )
    return jsonify(resultado)

# rota p remover jogos
@app.route("/jogos/<int:game_id>", methods=["DELETE"])
def remover_jogos(game_id):
    resultado = remove_game(game_id)
    return jsonify(resultado)

# rota recomendações
@app.route("/recomendacoes/<int:game_id>", methods=["GET"])
def recomendacoes(game_id):
    return jsonify({"game_id": game_id})

@app.route("/config")
def config():
    return jsonify({"rawg_key": os.getenv("RAWG_KEY")})

# rota p ver listas
@app.route("/listas", methods=["GET"])
def listar_listas():
    return jsonify(get_lists())

# rota p criar
@app.route("/listas", methods=["POST"])
def criar_lista():
    dados = request.get_json()
    resultado = add_list(dados["nome"])
    return jsonify(resultado)

# rota p apagar
@app.route("/listas/<nome>", methods=["DELETE"])
def deletar_lista(nome):
    resultado = remove_list(nome)
    return jsonify(resultado)

if __name__ == "__main__":
    app.run(debug=True)
