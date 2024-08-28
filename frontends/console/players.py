import re
from checkers.game.players import Player
from checkers.logic.exceptions import InvalidMove
from checkers.logic.models import GameState, Move

class ConsolePlayer(Player):
    def choose_move(self, game_state: GameState) -> Move | None:
        while not game_state.game_over:
            try:
                user_input = input(f"{self.piece}'s move (e.g., A1 to B2): ").strip()
                from_grid, to_grid = user_input.split(" to ")
                
                from_index = grid_to_index(from_grid)
                to_index = grid_to_index(to_grid)
                
                move = self.find_move_from_indices(game_state, from_index, to_index)
                if move:
                    return move
                print("No valid move found for the given coordinates.")
            except ValueError:
                print("Invalid coordinates format. Use A1 to B2, etc.")
            except InvalidMove:
                print("Invalid move. Please try again.")
        return None
    
    def find_move_from_indices(self, game_state: GameState, from_index: int, to_index: int) -> Move | None:
        for move in game_state.possible_moves:
            move_from_index = grid_to_index(f"{chr(move.from_col + ord('A'))}{move.from_row + 1}")
            move_to_index = grid_to_index(f"{chr(move.to_col + ord('A'))}{move.to_row + 1}")
            if move_from_index == from_index and move_to_index == to_index:
                return move
        return None

    def apply_move(self, game_state: GameState, move: Move) -> GameState:
        if self.piece == game_state.current_turn:
            return game_state.apply_move(
                from_row=move.from_row,
                from_col=move.from_col,
                to_row=move.to_row,
                to_col=move.to_col
            )
        else:
            raise InvalidMove("It's not your turn")

def grid_to_index(grid: str) -> int:
    if re.match(r"[a-hA-H][1-8]", grid):
        col, row = grid[0].upper(), grid[1]
    else:
        raise ValueError("Invalid grid coordinates. Use format A1 to H8.")

    row = int(row) - 1  

    if not ('A' <= col <= 'H') or not (0 <= row <= 7):
        raise ValueError("Invalid grid coordinates. Column should be A-H and row should be 1-8.")

    col_index = ord(col) - ord('A')
    row_index = row 

    return row_index * 8 + col_index

