# checkers/move.py

class Move:
    def __init__(self, start_position, end_position):
        self.start_position = start_position
        self.end_position = end_position

    def __str__(self):
        start_col, start_row = chr(self.start_position[1] + ord('A')), self.start_position[0] + 1
        end_col, end_row = chr(self.end_position[1] + ord('A')), self.end_position[0] + 1
        return f"{start_col}{start_row} -> {end_col}{end_row}"
