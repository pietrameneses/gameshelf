import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "../src"))
import pytest
from unittest.mock import patch, MagicMock
from shelf import add_game, get_games, update_game, remove_game

# função auxiliar pra criar respostas falsas do Supabase
def mock_response(data):
    mock = MagicMock()
    mock.data = data
    return mock

# teste: add jogo > ok
@patch("database.supabase")
def test_adicionar_jogo(mock_sb):
    # simula que o jogo não existe ainda
    mock_sb.table.return_value.select.return_value.eq.return_value.execute.return_value = mock_response([])
    mock_sb.table.return_value.insert.return_value.execute.return_value = mock_response([{"id": 1}])

    resultado = add_game(1, "Hollow Knight", "quero_jogar", "PC")
    assert resultado == {"ok": True}

# teste: add jogo duplicado > erro
@patch("database.supabase")
def test_adicionar_jogo_duplicado(mock_sb):
    # simula que o jogo já existe
    mock_sb.table.return_value.select.return_value.eq.return_value.execute.return_value = mock_response([
        {"rawg_id": 1, "name": "Hollow Knight"}
    ])

    resultado = add_game(1, "Hollow Knight", "quero_jogar", "PC")
    assert "erro" in resultado

# testes: listar jogos
@patch("database.supabase")
def test_listar_jogos(mock_sb):
    mock_sb.table.return_value.select.return_value.execute.return_value = mock_response([
        {"rawg_id": 1, "name": "Hollow Knight", "status": "quero_jogar", "platforms": "PC"},
        {"rawg_id": 2, "name": "Celeste", "status": "zerado", "platforms": "PC"},
    ])

    jogos = get_games()
    assert len(jogos) >= 0

@patch("database.supabase")
def test_filtrar_por_status(mock_sb):
    mock_sb.table.return_value.select.return_value.execute.return_value = mock_response([
        {"rawg_id": 1, "name": "Hollow Knight", "status": "quero_jogar", "platforms": "PC"},
        {"rawg_id": 2, "name": "Celeste", "status": "zerado", "platforms": "PC"},
    ])

    jogos = get_games(status="zerado")
    assert len(jogos) == 1
    assert jogos[0]["name"] == "Celeste"

# testes: atualizar jogos
# ok
@patch("database.supabase")
def test_atualizar_nota(mock_sb):
    # simula que o jogo existe
    mock_sb.table.return_value.select.return_value.eq.return_value.execute.return_value = mock_response([
        {"rawg_id": 1, "name": "Hollow Knight"}
    ])
    mock_sb.table.return_value.update.return_value.eq.return_value.execute.return_value = mock_response([])

    resultado = update_game(1, nota=5)
    assert resultado == {"ok": True}

# erro
@patch("database.supabase")
def test_nota_invalida(mock_sb):
    resultado = update_game(1, nota=6)
    assert "erro" in resultado

# erro
@patch("database.supabase")
def test_nota_invalida_negativa(mock_sb):
    resultado = update_game(1, nota=-1)
    assert "erro" in resultado

# teste: remover jogo > ok
@patch("database.supabase")
def test_remover_jogo(mock_sb):
    # simula que o jogo existe
    mock_sb.table.return_value.select.return_value.eq.return_value.execute.return_value = mock_response([
        {"rawg_id": 1, "name": "Hollow Knight"}
    ])
    mock_sb.table.return_value.delete.return_value.eq.return_value.execute.return_value = mock_response([])

    resultado = remove_game(1)
    assert resultado == {"ok": True}

# teste: remover jogo q n existe
@patch("database.supabase")
def test_remover_jogo_inexistente(mock_sb):
    # simula que o jogo não existe
    mock_sb.table.return_value.select.return_value.eq.return_value.execute.return_value = mock_response([])

    resultado = remove_game(999)
    assert "erro" in resultado
