import enum
from dataclasses import dataclass
from functools import cached_property

from checkers.logic.exceptions import InvalidMove
from checkers.logic.validators import validate_game_state, validate_grid, validate_start, validate_winner

class Piece(enum.StrEnum):
    BLACK = "b"
    RED = "r"
    BLACK_KING = "B"
    RED_KING = "R"

    @property
    def other(self) -> "Piece":
        return Piece.RED if self in [Piece.BLACK, Piece.BLACK_KING] else Piece.BLACK
    
    @property
    def is_king(self) -> bool:
        return self in [Piece.BLACK_KING, Piece.RED_KING]

    def promote(self) -> "Piece":
        if self == Piece.BLACK:
            return Piece.BLACK_KING
        elif self == Piece.RED:
            return Piece.RED_KING
        return self

@dataclass(frozen=True)
class Grid:
    cells: list[list[str]]

    def __post_init__(self) -> None:
        validate_grid(self)  

    @cached_property
    def r_count(self) -> int:
        return sum(row.count("r") + row.count("R") for row in self.cells)
    
    @cached_property
    def b_count(self) -> int:
        return sum(row.count("b") + row.count("B") for row in self.cells)
    
    @cached_property
    def empty_count(self) -> int:
        return sum(row.count(" ") for row in self.cells)

    @staticmethod
    def initial_setup() -> list[list[str]]:
        return [
            [" ", "b", " ", "b", " ", "b", " ", "b"],  # Row 0
            ["b", " ", "b", " ", "b", " ", "b", " "],  # Row 1
            [" ", "b", " ", "b", " ", "b", " ", "b"],  # Row 2
            [" ", " ", " ", " ", " ", " ", " ", " "],  # Row 3 (empty)
            [" ", " ", " ", " ", " ", " ", " ", " "],  # Row 4 (empty)
            ["r", " ", "r", " ", "r", " ", "r", " "],  # Row 5
            [" ", "r", " ", "r", " ", "r", " ", "r"],  # Row 6
            ["r", " ", "r", " ", "r", " ", "r", " "],  # Row 7
        ]

    @classmethod
    def default(cls) -> "Grid":
        return cls(cls.initial_setup())

@dataclass(frozen=True)
class Move:
    piece: Piece
    from_row: int
    from_col: int
    to_row: int
    to_col: int
    before_state: "GameState"
    after_state: "GameState"

@dataclass
class GameState:
    grid: Grid
    current_turn: Piece = Piece.BLACK

    @property
    def next_turn(self) -> Piece:
        return self.current_turn.other

    @property
    def game_not_started(self) -> bool:
        return self.grid.cells == Grid.initial_setup()

    @property
    def game_over(self) -> bool:
        if self.grid.b_count == 0:
            return True
        elif self.grid.r_count == 0:
            return True

        if self.has_valid_moves(self.current_turn) is False:
            return True

        return False

    @property
    def winner(self) -> Piece:
        if self.grid.b_count == 0:
            return Piece.RED
        elif self.grid.r_count == 0:
            return Piece.BLACK
        
        if self.has_valid_moves(self.current_turn) is False:
            return self.current_turn.other
        
        return None

    def has_valid_moves(self, player: Piece) -> bool:
        for row in range(8):
            for col in range(8):
                cell = self.grid.cells[row][col]
                if self.is_player_piece(cell, player):
                    if self.find_valid_moves(row, col, cell) != []:
                        return True
        return False

    def is_player_piece(self, cell: str, player: Piece) -> bool:
        if player == Piece.BLACK or player == Piece.BLACK_KING:
            return cell in [Piece.BLACK.value, Piece.BLACK_KING.value]
        elif player == Piece.RED or player == Piece.RED_KING:
            return cell in [Piece.RED.value, Piece.RED_KING.value]
        return False
    
    def find_valid_moves(self, row: int, col: int, piece: Piece) -> list[tuple[int, int]]:
        def explore_jumps(r, c, visited):
            jumps = []
            for dr, dc in directions:
                jump_r, jump_c = r + 2 * dr, c + 2 * dc
                mid_r, mid_c = r + dr, c + dc

                if (0 <= jump_r < 8 and 0 <= jump_c < 8 and
                    self.grid.cells[jump_r][jump_c] == " " and
                    self.grid.cells[mid_r][mid_c] in [Piece.RED.value, Piece.RED_KING.value, Piece.BLACK.value, Piece.BLACK_KING.value] and
                    self.is_opponent_piece(self.grid.cells[mid_r][mid_c])):
                    
                    if (jump_r, jump_c) not in visited:
                        visited.add((jump_r, jump_c))
                        jumps.append((jump_r, jump_c))
                        jumps.extend(explore_jumps(jump_r, jump_c, visited))
            return jumps

        normal_moves = []
        jump_moves = []

        if piece == Piece.BLACK:
            directions = [(1, -1), (1, 1)]
        elif piece == Piece.RED:
            directions = [(-1, -1), (-1, 1)]
        elif piece in [Piece.BLACK_KING, Piece.RED_KING]:
            directions = [(1, -1), (1, 1), (-1, -1), (-1, 1)]

        for dr, dc in directions:
            r, c = row + dr, col + dc
            if 0 <= r < 8 and 0 <= c < 8:
                if self.grid.cells[r][c] == " ":
                    normal_moves.append((r, c))
                elif self.is_opponent_piece(self.grid.cells[r][c]):
                    jump_r, jump_c = r + dr, c + dc
                    if 0 <= jump_r < 8 and 0 <= jump_c < 8 and self.grid.cells[jump_r][jump_c] == " ":
                        normal_moves.append((jump_r, jump_c))

        visited = set()
        jump_moves.extend(explore_jumps(row, col, visited))

        all_moves = set(normal_moves) | set(jump_moves)

        return list(all_moves)

    def is_opponent_piece(self, cell: str) -> bool:
        if self.current_turn == Piece.BLACK or self.current_turn == Piece.BLACK_KING:
            return cell in [Piece.RED.value, Piece.RED_KING.value]
        elif self.current_turn == Piece.RED or self.current_turn == Piece.RED_KING:
            return cell in [Piece.BLACK.value, Piece.BLACK_KING.value]
        return False

    def apply_move(self, from_row: int, from_col: int, to_row: int, to_col: int) -> Move:
        if self.grid.cells[from_row][from_col] == " ":
            raise InvalidMove("Source cell is empty")
        if self.grid.cells[to_row][to_col] != " ":
            raise InvalidMove("Destination cell is not empty")
        
        new_cells = [row[:] for row in self.grid.cells]
        
        new_cells[to_row][to_col] = new_cells[from_row][from_col]
        new_cells[from_row][from_col] = " "
        
        if abs(from_row - to_row) == 2 and abs(from_col - to_col) == 2:
            jumped_row = (from_row + to_row) // 2
            jumped_col = (from_col + to_col) // 2
            new_cells[jumped_row][jumped_col] = " "
        
        if to_row == 0 and new_cells[to_row][to_col] == Piece.RED.value:
            new_cells[to_row][to_col] = Piece.RED_KING.value
        elif to_row == 7 and new_cells[to_row][to_col] == Piece.BLACK.value:
            new_cells[to_row][to_col] = Piece.BLACK_KING.value
            
        new_grid = Grid(new_cells)
        new_game_state = GameState(grid=new_grid, current_turn=self.next_turn)
        
        return Move(
            piece=self.current_turn,
            from_row=from_row,
            from_col=from_col,
            to_row=to_row,
            to_col=to_col,
            before_state=self,
            after_state=new_game_state
        )

    @property
    def possible_moves(self) -> list[Move]:
        moves = []
        for row in range(8):
            for col in range(8):
                cell = self.grid.cells[row][col]
                if self.is_player_piece(cell, self.current_turn):
                    valid_moves = self.find_valid_moves(row, col, cell)
                    for (to_row, to_col) in valid_moves:
                        try:
                            new_grid = self.apply_move(row, col, to_row, to_col)
                            moves.append(Move(
                                piece=self.current_turn,
                                from_row=row,
                                from_col=col,
                                to_row=to_row,
                                to_col=to_col,
                                before_state=self,
                                after_state=GameState(grid=new_grid, current_turn=self.next_turn)
                            ))
                        except InvalidMove as e:
                            print(f"Invalid move attempted: {e}")
        return moves
