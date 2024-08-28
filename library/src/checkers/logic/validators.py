from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from checkers.logic.models import GameState, Grid, Piece

from checkers.logic.exceptions import InvalidGameState

def validate_game_state(game_state: GameState) -> None:
    validate_grid(game_state.grid)
    validate_start(game_state.grid)
    validate_winner(game_state.grid, game_state.winner)

def validate_grid(grid: Grid) -> None:
    if len(grid.cells) != 8 or any(len(row) != 8 for row in grid.cells):
        raise ValueError("Invalid grid: must be an 8x8 matrix.")

    valid_chars = {" ", "r", "b"}
    for row in grid.cells:
        if not all(cell in valid_chars for cell in row):
            raise ValueError("Invalid grid: cells must only contain spaces, 'r', or 'b'.")

def validate_start(grid: Grid, current_turn: Piece) -> None:
    if grid.b_count != 12 or grid.r_count != 12:
        raise InvalidGameState("Invalid starting configuration: must have 12 black and 12 red pieces.")

def validate_winner(grid: Grid, winner: Piece) -> None:
    if winner is not None:
        if winner not in (Piece.BLACK, Piece.RED):
            raise InvalidGameState("Invalid winner: must be either Black or Red.")
        if (winner == Piece.BLACK and grid.b_count != 0) or \
           (winner == Piece.RED and grid.r_count != 0):
            raise InvalidGameState("Invalid winner: the winner's color must have no remaining pieces.")
