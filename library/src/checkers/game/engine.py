from dataclasses import dataclass
from typing import Callable, TypeAlias

from checkers.game.players import Player
from checkers.game.renderers import Renderer
from checkers.logic.exceptions import InvalidMove
from checkers.logic.models import GameState, Grid, Piece, Move
from checkers.logic.validators import validate_players

ErrorHandler: TypeAlias = Callable[[Exception], None]

@dataclass(frozen=True)
class Checkers:
    player1: Player
    player2: Player
    renderer: Renderer
    error_handler: ErrorHandler | None = None

    def __post_init__(self):
        validate_players(self.player1, self.player2)

    def play(self) -> None:
        game_state = GameState(Grid.default())
        while True:
            self.renderer.render(game_state)
            if game_state.game_over:
                self.renderer.render(game_state)
                winner = game_state.winner
                if winner:
                    print(f"Game over! Winner: {winner.name}")
                else:
                    print("Game over! It's a draw.")
                break
            
            player = self.get_current_player(game_state)
            try:
                move = player.choose_move(game_state)
                game_state = self.apply_move(game_state, move)
            except InvalidMove as e:
                if self.error_handler:
                    self.error_handler(e)

    def get_current_player(self, game_state: GameState) -> Player:
        if game_state.current_turn == Piece.BLACK:
            return self.player1
        else:
            return self.player2

    def apply_move(self, game_state: GameState, move: Move) -> GameState:
        if move not in game_state.possible_moves:
            raise InvalidMove("Move is not valid in the current game state.")
        
        new_game_state = game_state.apply_move(move.from_row, move.from_col, move.to_row, move.to_col).after_state
        return new_game_state
