# utils.py

from checkers.move import Move

def position_to_coordinates(position):
    """ Convert board position (e.g., 'A1') to board coordinates (e.g., (0, 0)). """
    column, row = position[0], position[1]
    column_index = ord(column.upper()) - ord('A')
    row_index = int(row) - 1
    return (row_index, column_index)

def get_player_move(board):
    """Get a valid move from the player."""
    while True:
        start = input("Enter start position (e.g., 'A1'): ")
        end = input("Enter end position (e.g., 'B2'): ")
        start_pos = parse_position(start)
        end_pos = parse_position(end)
        move = Move(start_pos, end_pos)
        
        if board.is_valid_move(move):
            print(f"Player move: {move}")
            return move
        print("Invalid move. Try again.")

def parse_position(position):
    """Convert position like 'A1' into tuple (row, col)."""
    col = ord(position[0].upper()) - ord('A')
    row = int(position[1]) - 1
    return (row, col)
