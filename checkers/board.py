# checkers/board.py

import copy

from checkers.move import Move

class Board:
    def __init__(self):
        self.board = self.create_initial_board()
        self.black = 12
        self.red = 12
        self.black_king = 0
        self.red_king = 0
        self.current_player = "black"

    def create_initial_board(self):
        board = [[None for _ in range(8)] for _ in range(8)]
        
        for row in range(3):
            for col in range((row % 2), 8, 2):
                board[row][col] = 'B'  
        
        for row in range(5, 8):
            for col in range((row % 2), 8, 2):
                board[row][col] = 'R' 
        
        return board

    def display(self):
        """ Display the board state. """
        header = "    A   B   C   D   E   F   G   H"
        separator = "  +" + "---+" * 8
        rows = []

        for i, row in enumerate(self.board):
            row_str = f"{i + 1} |" + "|".join(
                f" {cell if cell else ' '} " for cell in row
            ) + "|"
            rows.append(row_str)
        
        print(f"{header}\n{separator}\n" + f"\n{separator}\n".join(rows) + f"\n{separator}\n")

    def is_valid_move(self, move):
        start_x, start_y = move.start_position
        end_x, end_y = move.end_position
        
        if not (0 <= start_x < 8 and 0 <= start_y < 8 and 0 <= end_x < 8 and 0 <= end_y < 8):
            return False
        
        piece = self.board[start_x][start_y]
        target = self.board[end_x][end_y]

        if piece is None or target is not None:
            return False

        dx = abs(end_x - start_x)
        dy = abs(end_y - start_y)

        if dx != dy or dx == 0:
            return False

        if piece == 'B' and end_x <= start_x and piece != 'BK':
            return False
        if piece == 'R' and end_x >= start_x and piece != 'RK':
            return False

        if dx == 2:
            mid_x = (start_x + end_x) // 2
            mid_y = (start_y + end_y) // 2
            mid_piece = self.board[mid_x][mid_y]
            if mid_piece is None or mid_piece in [piece, piece.upper()]:
                return False
        
        if dx == 1 and piece not in ['BK', 'RK'] and not (piece == 'B' and end_x > start_x) and not (piece == 'R' and end_x < start_x):
            return True

        if piece in ['BK', 'RK']:
            return True

        return True

    def apply_move(self, move):
        start_x, start_y = move.start_position
        end_x, end_y = move.end_position
        piece = self.board[start_x][start_y]
        self.board[end_x][end_y] = piece
        self.board[start_x][start_y] = None

        if abs(end_x - start_x) == 2:
            mid_x = (start_x + end_x) // 2
            mid_y = (start_y + end_y) // 2
            jumped_piece = self.board[mid_x][mid_y]
            self.board[mid_x][mid_y] = None
            if jumped_piece == 'B' or jumped_piece == 'BK':
                self.black -= 1
            elif jumped_piece == 'R' or jumped_piece == 'RK':
                self.red -= 1

        if piece == 'B' and end_x == 7:
            self.board[end_x][end_y] = 'BK'
            self.black_king += 1
            self.black -= 1
        elif piece == 'R' and end_x == 0:
            self.board[end_x][end_y] = 'RK'
            self.red_king += 1
            self.red -= 1

        additional_jumps = self.get_possible_jumps(end_x, end_y)
        while additional_jumps:
            next_jump = additional_jumps[0]
            self.apply_move(next_jump)
            additional_jumps = self.get_possible_jumps(next_jump.end_position[0], next_jump.end_position[1])

    def get_possible_moves(self):
        possible_moves = []
        player_pieces = ['B', 'BK'] if self.current_player == "black" else ['R', 'RK']
        directions = [(-1, -1), (-1, 1), (1, -1), (1, 1)] 

        for x in range(8):
            for y in range(8):
                piece = self.board[x][y]
                if piece not in player_pieces:
                    continue

                for dx, dy in directions:
                    new_x, new_y = x + dx, y + dy

                    if 0 <= new_x < 8 and 0 <= new_y < 8 and self.board[new_x][new_y] is None:
                        if (piece == 'B' and new_x > x) or (piece == 'R' and new_x < x) or piece in ['BK', 'RK']:
                            possible_moves.append(Move((x, y), (new_x, new_y)))

                    jump_x, jump_y = x + 2 * dx, y + 2 * dy
                    if 0 <= jump_x < 8 and 0 <= jump_y < 8 and self.board[jump_x][jump_y] is None:
                        mid_piece = self.board[x + dx][y + dy]
                        if mid_piece and mid_piece not in player_pieces:
                            possible_moves.append(Move((x, y), (jump_x, jump_y)))

        return possible_moves
    
    def get_possible_jumps(self, x, y):
        piece = self.board[x][y]
        if piece is None:
            return []

        possible_jumps = []
        opponent_pieces = ['R', 'RK'] if piece in ['B', 'BK'] else ['B', 'BK']
        directions = [(-1, -1), (-1, 1), (1, -1), (1, 1)]

        for dx, dy in directions:
            mid_x = x + dx
            mid_y = y + dy
            end_x = x + 2 * dx
            end_y = y + 2 * dy

            if 0 <= end_x < 8 and 0 <= end_y < 8:
                mid_piece = self.board[mid_x][mid_y]
                end_square = self.board[end_x][end_y]

                if mid_piece in opponent_pieces and end_square is None:
                    possible_jumps.append(Move((x, y), (end_x, end_y)))

        return possible_jumps

    def game_over(self):
        return self.black == 0 or self.red == 0 or not self.get_possible_moves()

    def evaluate_game_score(self):
        score = 0
        for row in self.board:
            for cell in row:
                if cell == 'B':
                    score += 1
                elif cell == 'R':
                    score -= 1
                elif cell == 'BK':
                    score += 2
                elif cell == 'RK':
                    score -= 2
        return score
    
    def evaluate_board(self):
        score = 0
        
        piece_values = {'B': 1, 'R': -1, 'BK': 2, 'RK': -2}
        
        for row in range(8):
            for col in range(8):
                piece = self.board[row][col] 
                if piece:
                    score += piece_values.get(piece, 0)
        
        return score

    def copy(self):
        return copy.deepcopy(self)
    
    def find_best_move(self, board, depth):
        best_move = None
        best_value = float('-inf')
        possible_moves = self.get_possible_moves()  
        
        for move in possible_moves:
            board_copy = board.copy() 
            board_copy.apply_move(move)
            move_value = self.minmax(board_copy, depth - 1, float('-inf'), float('inf'), False)
            print(f"Move: {move}, Move value: {move_value}")
            
            if move_value > best_value:
                best_value = move_value
                best_move = move
        
        print(f"Best move: {best_move}")
        return best_move

    def minmax(self, board, depth, alpha, beta, maximizing_player):
        if depth == 0 or self.game_over():
            return self.evaluate_board()
        
        if maximizing_player:
            max_eval = float('-inf')
            for move in self.get_possible_moves():
                board_copy = board.copy() 
                board_copy.apply_move(move)
                eval = self.minmax(board_copy, depth - 1, alpha, beta, False)
                max_eval = max(max_eval, eval)
                alpha = max(alpha, eval)
                if beta <= alpha:
                    break
            return max_eval
        else:
            min_eval = float('inf')
            for move in self.get_possible_moves(): 
                board_copy = board.copy()
                board_copy.apply_move(move)
                eval = self.minmax(board_copy, depth - 1, alpha, beta, True)
                min_eval = min(min_eval, eval)
                beta = min(beta, eval)
                if beta <= alpha:
                    break
            return min_eval

