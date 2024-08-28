import textwrap
from typing import Iterable, List, Optional, TextIO

from checkers.game.renderers import Renderer
from checkers.logic.models import GameState

class ConsoleRenderer(Renderer):
    def __init__(self, file_path: Optional[str] = None) -> None:
        self.file_path = file_path
        self.history: List[str] = [] 

    def render(self, game_state: GameState) -> None:
        board_str = self.get_board_string(game_state)
        if self.file_path:
            self.history.append(board_str)
            with open(self.file_path, 'w') as file:
                file.write("\n\n".join(self.history))
                if game_state.winner:
                    file.write(f"\n{game_state.winner} wins \N{party popper}\n")
        else:
            print(board_str)
            if game_state.winner:
                print(f"{game_state.winner} wins \N{party popper}")

    def get_board_string(self, game_state: GameState) -> str:
        header = "    A   B   C   D   E   F   G   H"
        separator = "  +" + "---+" * 8

        rows = []
        for i, row in enumerate(game_state.grid.cells):
            row_str = f"{i + 1} |" + "|".join(f" {cell if cell else "  "} " for cell in row) + "|"
            rows.append(row_str)

        return f"{header}\n{separator}\n" + f"\n{separator}\n".join(rows) + f"\n{separator}"

def clear_screen() -> None:
    print("\033c", end="")

def blink(text: str) -> str:
    return f"\033[5m{text}\033[0m"

def print_solid(cells: list[list[str]], file: Optional[TextIO] = None) -> None:
    header = "   A B C D E F G H"
    separator = "  +" + "-+-" * 8

    rows = []
    for i, row in enumerate(cells):
        row_str = f"{i + 1} " + " | ".join(f"{cell}" if cell else " " for cell in row)
        rows.append(row_str)

    board_str = f"{header}\n{separator}\n" + f"\n{separator}\n".join(rows) + f"\n{separator}"

    if file:
        file.write(board_str + "\n")
    else:
        print(board_str)