from checkers.logic.models import GameState, Grid, Piece

def test_initial_game_state():
    game_state = GameState(Grid.default())
    
    assert game_state.game_not_started is True
    assert game_state.game_over is False
    assert game_state.winner is None
    assert len(game_state.possible_moves) > 0 

def test_specific_game_state():
    custom_grid = [
        [" ", " ", " ", " ", " ", " ", " ", " "],
        [" ", " ", " ", " ", " ", " ", " ", " "],
        [" ", " ", " ", " ", " ", " ", " ", " "],
        [" ", "r", " ", " ", " ", " ", " ", " "],
        [" ", " ", " ", "b", " ", " ", " ", " "],
        [" ", " ", " ", " ", " ", " ", " ", " "],
        [" ", " ", " ", " ", " ", " ", " ", " "],
        [" ", " ", " ", " ", " ", " ", " ", " "],
    ]
    game_state = GameState(Grid(custom_grid), current_turn=Piece.BLACK)
    
    assert game_state.current_turn == Piece.BLACK
    moves = game_state.find_valid_moves(4, 3, Piece.BLACK)
    assert moves == [(5, 2), (5, 4)]

def test_next_turn():
    game_state = GameState(Grid.default())
    
    assert game_state.next_turn is Piece.RED
    
def test_game_over():
    custom_grid = [
        [" ", " ", " ", " ", " ", " ", " ", " "],
        [" ", " ", " ", " ", " ", " ", " ", " "],
        [" ", " ", " ", " ", " ", " ", " ", " "],
        [" ", " ", " ", " ", " ", " ", " ", " "],
        [" ", " ", " ", " ", " ", " ", " ", " "],
        [" ", " ", " ", " ", " ", " ", " ", " "],
        [" ", " ", " ", " ", " ", " ", " ", " "],
        [" ", " ", " ", " ", "r", " ", " ", " "],
    ]
    game_state = GameState(Grid(custom_grid), current_turn=Piece.BLACK)
    
    assert game_state.game_over is True
    assert game_state.winner == Piece.RED

def test_winner_by_no_pieces():
    custom_grid = [
        [" ", " ", " ", " ", " ", " ", " ", " "],
        [" ", " ", " ", " ", " ", " ", " ", " "],
        [" ", " ", " ", " ", " ", " ", " ", " "],
        [" ", " ", " ", " ", " ", " ", " ", " "],
        [" ", " ", " ", " ", " ", " ", " ", " "],
        ["b", " ", "b", " ", "b", " ", "b", " "],
        [" ", "b", " ", "b", " ", "b", " ", "b"],
        ["b", " ", "b", " ", "b", " ", "b", " "],
    ]
    game_state = GameState(Grid(custom_grid), current_turn=Piece.BLACK)
    
    assert game_state.game_over is True
    assert game_state.winner == Piece.BLACK

def test_winner_by_no_moves():
    custom_grid = [
        [" ", " ", " ", " ", " ", " ", " ", " "],
        ["r", " ", "r", " ", "r", " ", "r", " "],
        [" ", "r", " ", "r", " ", "r", " ", "r"],
        ["r", " ", "r", " ", "r", " ", "r", " "],
        [" ", " ", " ", " ", " ", " ", " ", " "],
        [" ", " ", " ", " ", " ", " ", " ", " "],
        [" ", " ", " ", " ", " ", " ", " ", " "],
        [" ", " ", " ", " ", " ", " ", " ", " "],
    ]
    game_state = GameState(Grid(custom_grid), current_turn=Piece.BLACK)
    
    assert game_state.game_over is True
    assert game_state.winner == Piece.RED

def test_jump_move():
    custom_grid = [
        [" ", " ", " ", " ", " ", " ", " ", " "],
        [" ", " ", " ", " ", " ", " ", " ", " "],
        [" ", " ", " ", " ", " ", " ", " ", " "],
        [" ", " ", " ", " ", " ", " ", " ", " "],
        [" ", " ", "b", " ", " ", " ", " ", " "], 
        [" ", " ", " ", "r", " ", " ", " ", " "], 
        [" ", " ", " ", " ", " ", " ", " ", " "], 
        [" ", " ", " ", " ", " ", " ", " ", " "], 
    ]
    game_state = GameState(Grid(custom_grid), current_turn=Piece.BLACK)

    assert game_state.current_turn == Piece.BLACK
    moves = game_state.find_valid_moves(4, 2, Piece.BLACK)
    assert moves == [(5, 1), (6, 4)]

if __name__ == "__main__":
    test_initial_game_state()
    test_specific_game_state()
    test_next_turn()
    test_game_over()
    test_winner_by_no_pieces()
    test_winner_by_no_moves()
    test_jump_move()
    print("All tests passed!")
