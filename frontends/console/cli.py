from checkers.game.engine import Checkers

from .args import parse_args
from .renderers import ConsoleRenderer

def main() -> None:
    player1, player2, starting_player = parse_args()
    Checkers(player1, player2, ConsoleRenderer()).play()
