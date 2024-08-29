# app.py

from flask import Flask, render_template, request, jsonify
from checkers.board import Board
from checkers.move import Move
from utils import position_to_coordinates

app = Flask(__name__)

board = Board()

@app.route('/')
def index():
    return render_template('index.html', board=board.board)

@app.route('/reset', methods=['POST'])
def reset():
    global board
    board = Board()
    return jsonify({"board": board.board, "gameOver": False})

@app.route('/move', methods=['POST'])
def move():
    data = request.json
    start_pos = (data['startX'], data['startY'])
    end_pos = (data['endX'], data['endY'])

    player_move = Move(start_pos, end_pos)

    if board.is_valid_move(player_move):
        board.apply_move(player_move)
        board.current_player = 'red'

        # After player move, have the AI make a move
        ai_move = board.find_best_move(board, depth=3)
        if ai_move and board.is_valid_move(ai_move):
            board.apply_move(ai_move)
            board.current_player = 'black'
        else:
            return jsonify({"error": "AI failed to make a valid move"}), 500

        # Check if game is over
        game_over = board.game_over()
        return jsonify({"board": board.board, "gameOver": game_over})
    else:
        return jsonify({"error": "Invalid move"}), 400

if __name__ == "__main__":
    app.run(port=8000, debug=True)
