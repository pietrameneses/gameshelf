import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "../src"))

import pytest
from shelf import add_game, get_games, update_game, remove_game

import shelf

@pytest.fixture(autouse=True)
def usar_shelf_temporario(tmp_path):
    shelf.DATA_PATH = str(tmp_path / "test_shelf.json")

# teste: add jogo > ok
def test_adicionar_jogo():
    resultado = add_game(1, "Hollow Knight", "quero_jogar", "PC")
    assert resultado == {"ok": True}

# teste: add jogo duplicado > erro
def test_adicionar_jogo_duplicado():
    add_game(1, "Hollow Knight", "quero_jogar", "PC")
    resultado = add_game(1, "Hollow Knight", "quero_jogar", "PC")
    assert "erro" in resultado

# testes: listar jogos 
def test_listar_jogos():
    add_game(1, "Hollow Knight", "quero_jogar", "PC")
    add_game(2, "Celeste", "zerado", "PC")
    jogos = get_games()
    assert len(jogos) == 2
 
def test_filtrar_por_status():
    add_game(1, "Hollow Knight", "quero_jogar", "PC")
    add_game(2, "Celeste", "zerado", "PC")
    jogos = get_games(status="zerado")
    assert len(jogos) == 1
    assert jogos[0]["nome"] == "Celeste"
 
# testes: atualizar jogos

# ok
def test_atualizar_nota():
    add_game(1, "Hollow Knight", "quero_jogar", "PC")
    resultado = update_game(1, nota=5)
    assert resultado == {"ok": True}
 
# erro
def test_nota_invalida():
    add_game(1, "Hollow Knight", "quero_jogar", "PC")
    resultado = update_game(1, nota=6)
    assert "erro" in resultado

# erro
def test_nota_invalida_negativa():
    add_game(1, "Hollow Knight", "quero_jogar", "PC")
    resultado = update_game(1, nota=-1)
    assert "erro" in resultado

# teste: remover jogo > ok
def test_remover_jogo():
    add_game(1, "Hollow Knight", "quero_jogar", "PC")
    resultado = remove_game(1)
    assert resultado == {"ok": True}
 
# teste: remover jogo q n existe
def test_remover_jogo_inexistente():
    resultado = remove_game(999)
    assert "erro" in resultado