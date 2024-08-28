import argparse
from typing import NamedTuple

from checkers.game.players import Player, RandomComputerPlayer
from checkers.logic.models import Piece

from .players import ConsolePlayer

PLAYER_CLASSES = {
    "human": ConsolePlayer,
    "random": RandomComputerPlayer,
}

class Args(NamedTuple):
    player_black: Player
    player_red: Player
    starting_piece: Piece

def parse_args() -> Args:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-BLACK",
        dest="player_black",
        choices=PLAYER_CLASSES.keys(),
        default="human",
    )
    parser.add_argument(
        "-RED",
        dest="player_red",
        choices=PLAYER_CLASSES.keys(),
        default="random",
    )
    parser.add_argument(
        "--starting",
        dest="starting_piece",
        choices=[Piece.BLACK, Piece.RED],
        default=Piece.BLACK.value,
    )
    args = parser.parse_args()

    player1 = PLAYER_CLASSES[args.player_black](Piece.BLACK)
    player2 = PLAYER_CLASSES[args.player_red](Piece.RED)

    starting_piece = Piece(args.starting_piece)

    if starting_piece == Piece.RED:
        player1, player2 = player2, player1
    
    return Args(player1, player2, args.starting_piece)