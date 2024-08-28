from checkers.game.engine import Checkers
from checkers.game.players import RandomComputerPlayer
from checkers.logic.models import Piece

from console.players import ConsolePlayer
from console.renderers import ConsoleRenderer

# player1 = RandomComputerPlayer(Piece.BLACK)
player1 = ConsolePlayer(Piece.BLACK)
player2 = RandomComputerPlayer(Piece.RED)

renderer = ConsoleRenderer(file_path='game_output.txt')
game = Checkers(player1, player2, renderer)
game.play()