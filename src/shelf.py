# importar as bibliotecas q vão ser usadas
import json
import os
from datetime import date

# p/ fazer funcionar em qualquer os, montando um caminho de arquivos
DATA_PATH = os.path.join(os.path.dirname(__file__), "data", "shelf.json")

# função pra carregar/ler os dados do arq. json
def _load():
    # verificar se o caminho existe p/ poder ler e nn dar erro
    if not os.path.exists(DATA_PATH):
        return {"jogos":[]}
    # ler arquivo
    with open(DATA_PATH, "r", encoding="utf-8") as f:
        return json.load(f)
    
# salvar os dados no json
def _save(data): # precisa do (data) p/ salvar
    # garante se a pasta existe
    os.makedirs(os.path.dirname(DATA_PATH), exist_ok=True)
    # escrever no arquivo
    with open(DATA_PATH, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

# função mais complexa pra add jogos
def add_game(game_id, nome, status, plataforma):   # define os parâmetros a serem utilizados
    data = _load()   # data = dicionário c informações
    for jogo in data["jogos"]:               # procura se tem um jogo já com o mesmo id
        if jogo["id"] == game_id:            
            return {"erro": "Jogo já existe na shelf"}    # se tiver retorna erro
    novo_jogo = {                            # monta o dicionário do novo jogo a ser cadastrado
        "id": game_id,
        "nome": nome,
        "status": status,
        "plataforma": plataforma,
        "nota": None,
        "review": "",
        "horas": 0,
        "tags": [],
        "data_adicao": str(date.today())
    }    
    data["jogos"].append(novo_jogo)         # salva na lista
    _save(data)
    return {"ok": True}                     # verifica se foi

# outra função um pouco mais complexa rs pra pegar a lista de jogos filtrada
def get_games(status=None, plataforma=None):  # add parametros
    data = _load()   # carrega os dados
    jogos = data["jogos"]    # pega a lista dos jogos
    if status:
        jogos = [j for j in jogos if j["status"] == status] # filtra se o status foi informado ou nn
    if plataforma:
        jogos = [j for j in jogos if j["plataforma"] == plataforma] # filtra se a plataforma foi informada ou nn
    return jogos     # retorna a lista de jogos filtrada

# agora outra função pra atualizar os jogos já existentes
def update_game(game_id, nota=None, review=None, status=None, horas=None, tags=None):
    if nota is not None and (nota < 1 or nota > 5):      # verifica se foi informada
        return {"erro": "Nota deve ser entre 1 e 5"}     # se não foi, mostra erro
    data = _load()
    for jogo in data["jogos"]:
        if jogo["id"] == game_id:          # atualiza os parâmetros
            if nota is not None:
                jogo["nota"] = nota
            if review is not None:
                jogo["review"] = review
            if status is not None:
                jogo["status"] = status
            if horas is not None:
                jogo["horas"] = horas
            if tags is not None:
                jogo["tags"] = tags
            _save(data)
            return {"ok": True}


    return {"erro": "Jogo não encontrado"}  # se o jgo n for encontrado aparece esse erro

# agora uma função p remover jogos
def remove_game(game_id):
    data = _load()
    antes = len(data["jogos"])  # guarda o tamanho da lista antes de remover
    data["jogos"] = [j for j in data["jogos"] if j["id"] != game_id]   # recria a lista sem um item
    if len(data["jogos"]) == antes:
        return {"erro": "Jogo não encontrado"}