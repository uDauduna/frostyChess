from training import apply_uci, clone, legal_actions, new_game, state_fen


def test_training_api_is_ui_independent():
    game = new_game()
    assert len(legal_actions(game)) == 20
    original = state_fen(game)
    copied = clone(game)
    assert apply_uci(copied, "e2e4")
    assert state_fen(game) == original
    assert state_fen(copied) != original


def test_training_api_loads_and_reproduces_fen():
    fen = "4k3/8/8/8/8/8/4P3/4K3 w - - 0 1"
    game = new_game(fen)
    assert state_fen(game) == fen
