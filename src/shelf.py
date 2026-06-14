# importar as bibliotecas q vão ser usadas
from database import supabase

# função pra add jogos
def add_game(game_id, nome, status, plataforma, imagem=""):   # define os parâmetros a serem utilizados
    # verifica se o jogo já existe
    response = supabase.table("games").select("*").eq("rawg_id", game_id).execute()
    if response.data:
        return {"erro": "Jogo já existe na shelf"}    # se tiver retorna erro

    # monta o dicionário do novo jogo a ser cadastrado
    novo_jogo = {
        "rawg_id": game_id,
        "name": nome,
        "status": status,
        "platforms": plataforma,
        "cover_url": imagem,
        "nota": None,
        "review": "",
        "horas": 0,
    }
    supabase.table("games").insert(novo_jogo).execute()
    return {"ok": True}                     # verifica se foi

# função pra pegar a lista de jogos filtrada
def get_games(status=None, plataforma=None):  # add parametros
    # carrega os dados do banco
    response = supabase.table("games").select("*").execute()
    jogos = response.data    # pega a lista dos jogos

    if status:
        jogos = [j for j in jogos if j.get("status") == status] # filtra se o status foi informado ou nn
    if plataforma:
        jogos = [j for j in jogos if j.get("platforms") == plataforma] # filtra se a plataforma foi informada ou nn
    return jogos     # retorna a lista de jogos filtrada

# função pra atualizar os jogos já existentes
def update_game(game_id, nota=None, review=None, status=None, horas=None, tags=None):
    if nota is not None and (nota < 1 or nota > 5):      # verifica se foi informada
        return {"erro": "Nota deve ser entre 1 e 5"}     # se não foi, mostra erro

    # verifica se o jogo existe
    response = supabase.table("games").select("*").eq("rawg_id", game_id).execute()
    if not response.data:
        return {"erro": "Jogo não encontrado"}

    # monta apenas os campos que foram informados
    updates = {}
    if nota is not None:
        updates["nota"] = nota
    if review is not None:
        updates["review"] = review
    if status is not None:
        updates["status"] = status
    if horas is not None:
        updates["horas"] = horas

    if updates:
        supabase.table("games").update(updates).eq("rawg_id", game_id).execute()

    return {"ok": True}

# função p remover jogos
def remove_game(game_id):
    # verifica se o jogo existe antes de remover
    response = supabase.table("games").select("*").eq("rawg_id", game_id).execute()
    if not response.data:
        return {"erro": "Jogo não encontrado"}

    supabase.table("games").delete().eq("rawg_id", game_id).execute()
    return {"ok": True}

# função p add lista
def add_list(nome):
    # verifica se a lista já existe
    response = supabase.table("lists").select("*").eq("name", nome).execute()
    if response.data:
        return {"erro": "Lista já existe"}

    supabase.table("lists").insert({"name": nome}).execute()
    return {"ok": True}

# ver listas
def get_lists():
    response = supabase.table("lists").select("*").execute()
    return [lista["name"] for lista in response.data]

# apagar lista
def remove_list(nome):
    fixas = ["Quero Jogar", "Jogando", "Zerado"]
    if nome in fixas:
        return {"erro": "Não é possível remover listas fixas"}

    # verifica se a lista existe
    response = supabase.table("lists").select("*").eq("name", nome).execute()
    if not response.data:
        return {"erro": "Lista não encontrada"}

    supabase.table("lists").delete().eq("name", nome).execute()
    return {"ok": True}
