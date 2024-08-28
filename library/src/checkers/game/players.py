import abc
import random
import time

from checkers.logic.exceptions import InvalidMove
from checkers.logic.models import GameState, Piece, Move

class Player(metaclass=abc.ABCMeta):
    def __init__(self, piece) -> None:
        self.piece = piece

    def apply_move(self, game_state: GameState) -> GameState:
        if self.piece == game_state.current_turn:
            move = self.choose_move(game_state)
            if move:
                return self.apply_move(game_state)
            raise InvalidMove("No more possible moves")
        else:
            raise InvalidMove("It's not your turn")
    
    @abc.abstractmethod
    def choose_move(self, game_state: GameState) -> Move | None:
        """Return the current player's move in the given game state."""
        
# class Player(metaclass=abc.ABCMeta):
#     def __init__(self, piece: Piece) -> None:
#         self.piece = piece

#     def apply_move(self, game_state: GameState) -> GameState:
#         if self.piece != game_state.current_turn:
#             raise InvalidMove("It's not your turn")

#         move = self.get_move(game_state)
#         if move is None:
#             raise InvalidMove("No move was made")

#         return self.apply_move_to_state(game_state, move)

#     def apply_move_to_state(self, game_state: GameState, move: Move) -> GameState:
#         if move.piece != self.piece:
#             raise InvalidMove("The move does not belong to this player")

#         if move not in game_state.possible_moves:
#             raise InvalidMove("The move is not valid")

#         new_game_state = game_state.apply_move(
#             from_row=move.from_row,
#             from_col=move.from_col,
#             to_row=move.to_row,
#             to_col=move.to_col
#         )
#         return new_game_state

#     @abc.abstractmethod
#     def get_move(self, game_state: GameState) -> Move | None:
#         """Return the current player's move in the given game state."""

class ComputerPlayer(Player, metaclass=abc.ABCMeta):
    def __init__(self, piece: Piece, delay_seconds: float = 0.25) -> None:
        super().__init__(piece)
        self.delay_seconds = delay_seconds
    
    def get_move(self, game_state: GameState) -> Move | None:
        time.sleep(self.delay_seconds)
        return self.get_computer_move(game_state)

    @abc.abstractmethod
    def get_computer_move(self, game_state: GameState) -> Move | None:
        """Return the computer player's move in the given game state."""

# class RandomComputerPlayer(ComputerPlayer):
#     def get_computer_move(self, game_state: GameState) -> Move | None:
#         try:
#             return random.choice(game_state.possible_moves)
#         except IndexError:
#             return None

class RandomComputerPlayer(Player):
    def __init__(self, piece: Piece) -> None:
        super().__init__(piece)

    def choose_move(self, game_state: GameState) -> Move:
        possible_moves = game_state.possible_moves
        if not possible_moves:
            raise InvalidMove("No valid moves available")
        return random.choice(possible_moves)
