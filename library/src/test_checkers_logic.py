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
    assert (5, 2) in moves
    assert (5, 4) in moves

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
    assert (5, 1) in moves
    assert (6, 4) in moves

def test_king_promotion_red():
    custom_grid = [
        [" ", " ", " ", " ", " ", " ", " ", " "],
        [" ", " ", " ", " ", " ", " ", " ", " "],
        [" ", " ", " ", " ", " ", " ", " ", " "],
        [" ", " ", " ", " ", " ", " ", " ", " "],
        [" ", " ", " ", " ", " ", " ", " ", " "],
        [" ", " ", " ", " ", " ", " ", " ", " "],
        [" ", " ", " ", " ", " ", " ", " ", " "],
        [" ", " ", " ", " ", " ", " ", " ", "r"],
    ]
    game_state = GameState(Grid(custom_grid), current_turn=Piece.RED)

    move = game_state.apply_move(7, 7, 0, 0)
    new_grid = move.after_state.grid
    assert new_grid.cells[0][0] == Piece.RED_KING.value

def test_king_promotion_black():
    custom_grid = [
        [" ", " ", " ", " ", " ", " ", " ", " "],
        [" ", " ", " ", " ", " ", " ", " ", " "],
        [" ", " ", " ", " ", " ", " ", " ", " "],
        [" ", " ", " ", " ", " ", " ", " ", " "],
        [" ", " ", " ", " ", " ", " ", " ", " "],
        [" ", " ", " ", " ", " ", " ", " ", " "],
        [" ", " ", " ", " ", " ", " ", "b", " "],
        [" ", " ", " ", " ", " ", " ", " ", " "],
    ]
    game_state = GameState(Grid(custom_grid), current_turn=Piece.BLACK)

    move = game_state.apply_move(6, 6, 7, 7)
    new_grid = move.after_state.grid
    assert new_grid.cells[7][7] == Piece.BLACK_KING.value

def test_king_moves():
    custom_grid = [
        [" ", " ", " ", " ", " ", " ", " ", " "], 
        [" ", " ", " ", " ", " ", " ", " ", " "],
        [" ", " ", " ", " ", " ", " ", " ", " "],
        [" ", " ", " ", "R", " ", " ", " ", " "],
        [" ", " ", " ", " ", "b", " ", " ", " "],
        [" ", " ", " ", " ", " ", " ", " ", " "],
        [" ", " ", " ", " ", " ", " ", "b", " "],
        ["b", " ", " ", " ", " ", " ", " ", " "],
    ]
    game_state = GameState(Grid(custom_grid), current_turn=Piece.RED)

    moves = game_state.find_valid_moves(3, 3, Piece.RED_KING)
    assert (2, 2) in moves
    assert (2, 4) in moves
    assert (4, 2) in moves
    assert (5, 5) in moves
    assert (7, 7) in moves
    assert (4, 4) not in moves
    assert (6, 6) not in moves

def test_double_jump_and_king_move():
    custom_grid = [
        [" ", " ", " ", " ", " ", " ", " ", " "],
        [" ", " ", " ", "b", " ", " ", " ", " "],
        [" ", " ", " ", " ", " ", " ", " ", " "],
        [" ", " ", " ", "b", " ", " ", " ", " "],
        [" ", " ", "r", " ", " ", " ", " ", " "], 
        [" ", " ", " ", " ", " ", " ", " ", " "], 
        [" ", " ", " ", " ", " ", " ", " ", " "], 
        [" ", " ", " ", " ", " ", " ", " ", " "], 
    ]
    game_state = GameState(Grid(custom_grid), current_turn=Piece.RED)

    moves = game_state.find_valid_moves(4, 2, Piece.RED)
    assert (0, 2) in moves
    move = game_state.apply_move(4, 2, 0, 2) 
    new_grid = move.after_state.grid
    assert new_grid.cells[0][2] == Piece.RED_KING.value
    assert new_grid.cells[1][3] == " "
    assert new_grid.cells[3][3] == " "

if __name__ == "__main__":
    test_initial_game_state()
    test_specific_game_state()
    test_next_turn()
    test_game_over()
    test_winner_by_no_pieces()
    test_winner_by_no_moves()
    test_jump_move()
    test_king_promotion_red()
    test_king_promotion_black()
    test_king_moves()
    test_double_jump_and_king_move()
    print("All tests passed!")
