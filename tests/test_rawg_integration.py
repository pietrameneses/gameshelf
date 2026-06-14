import pytest
from unittest.mock import patch, MagicMock
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "../src"))
from app import app

@pytest.fixture
def client():
    app.config["TESTING"] = True
    with app.test_client() as client:
        yield client

@patch("database.supabase")
def test_adicionar_jogo_com_dados_da_rawg(mock_sb, client):
    """Simula busca na RAWG e cadastro do jogo retornado na shelf"""
    # simula que o jogo não existe no banco
    mock_sb.table.return_value.select.return_value.eq.return_value.execute.return_value = MagicMock(data=[])
    mock_sb.table.return_value.insert.return_value.execute.return_value = MagicMock(data=[{"id": 1}])

    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.json.return_value = {
        "results": [{
            "id": 3498,
            "name": "Grand Theft Auto V",
            "background_image": "https://media.rawg.io/media/games/gta5.jpg"
        }]
    }
    with patch("requests.get", return_value=mock_response):
        import requests
        params = {"key": "fake_key", "search": "GTA V", "page_size": 1}
        resposta = requests.get("https://api.rawg.io/api/games", params=params)
        dados = resposta.json()["results"][0]

    # agora cadastra o jogo encontrado na shelf
    resposta_post = client.post("/jogos", json={
        "game_id": dados["id"],
        "nome": dados["name"],
        "status": "quero_jogar",
        "plataforma": "PC",
        "imagem": dados["background_image"]
    })

    body = resposta_post.get_json()
    assert resposta_post.status_code == 200
    assert body.get("ok") == True

@patch("database.supabase")
def test_rawg_fora_do_ar_nao_quebra_app(mock_sb, client):
    """Garante que uma falha na RAWG não derruba a aplicação"""
    # simula banco vazio
    mock_sb.table.return_value.select.return_value.execute.return_value = MagicMock(data=[])

    mock_response = MagicMock()
    mock_response.status_code = 500
    with patch("requests.get", return_value=mock_response):
        import requests
        resposta = requests.get("https://api.rawg.io/api/games")

    assert resposta.status_code == 500
    resposta_app = client.get("/jogos")
    assert resposta_app.status_code == 200
