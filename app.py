# app.py

from flask import Flask, render_template, request, jsonify
from checkers.board import Board
from checkers.move import Move

app = Flask(__name__)

board = Board()

@app.route('/')
def index():
    return render_template('index.html', board=board.board)

@app.route('/reset', methods=['POST'])
def reset():
    global board
    board = Board()
    return jsonify({"board": board.board, "gameOver": False, "message": ""})

@app.route('/move', methods=['POST'])
def move():
    data = request.json
    start_pos = (data['startX'], data['startY'])
    end_pos = (data['endX'], data['endY'])

    player_move = Move(start_pos, end_pos)

    if board.is_valid_move(player_move):
        board.apply_move(player_move)
        board.current_player = 'red'

        if board.game_over():
            game_over = True
            winner_message = determine_winner()
            return jsonify({"board": board.board, "gameOver": game_over, "message": winner_message})

        ai_move = board.find_best_move(board, depth=3)
        if ai_move and board.is_valid_move(ai_move):
            board.apply_move(ai_move)
            board.current_player = 'black'
        else:
            return jsonify({"error": "AI failed to make a valid move"}), 500

        game_over = board.game_over()
        if game_over:
            winner_message = determine_winner()
            return jsonify({"board": board.board, "gameOver": game_over, "message": winner_message})

        return jsonify({"board": board.board, "gameOver": game_over, "message": ""})
    else:
        return jsonify({"error": "Invalid move"}), 400

def determine_winner():
    black_score = board.black + board.black_king * 2
    red_score = board.red + board.red_king * 2

    if board.black == 0:
        return f"Red wins! 🎉 Final Score - Black: {black_score}, Red: {red_score}"
    elif board.red == 0:
        return f"Black wins! 🎉 Final Score - Black: {black_score}, Red: {red_score}"
    elif not board.get_possible_moves():
        if board.current_player == 'black':
            return f"Red wins by default! 🎉 Final Score - Black: {black_score}, Red: {red_score}"
        else:
            return f"Black wins by default! 🎉 Final Score - Black: {black_score}, Red: {red_score}"


if __name__ == "__main__":
    app.run(port=8000, debug=True)
