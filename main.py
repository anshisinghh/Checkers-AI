# main.py

from checkers.board import Board
from utils import get_player_move

def main():
    board = Board()

    while not board.game_over():
        board.display()
        print(f"{board.current_player}'s turn")
        if board.current_player == 'red':
            move = board.find_best_move(board, depth=3)
        else:
            move = get_player_move(board)
        
        if not board.is_valid_move(move):
            print("Invalid move. Try again.")
            continue
        
        board.apply_move(move)
        
        board.current_player = 'red' if board.current_player == 'black' else 'black'
        print(f"{board.current_player}'s turn")

    if board.black == 0:
        print("Red wins! \N{party popper}")
    elif board.red == 0:
        print("Black wins! \N{party popper}")
    else:
        if not board.get_possible_moves():
            if board.current_player == 'black':
                print("Red wins by default! \N{party popper}")
            else:
                print("Black wins by default! \N{party popper}")
        else:
            print("The game ended in a draw! \N{shrug}")

    black_score = board.black + board.black_king * 2
    red_score = board.red + board.red_king * 2
    print(f"Final Score - Black: {black_score}, Red: {red_score}")

if __name__ == "__main__":
    main()
