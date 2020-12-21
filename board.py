import numpy as np
from exceptions import NextPiece, GameOver, DeadEndError


class Board:

    height = 10
    width = 10
    game_over = False

    _final = np.zeros(shape=(height, width))

    def __init__(self):
        self.current = np.zeros(shape=(self.height, self.width))

    @property
    def taken_fields(self):
        return [i for i in zip(*np.where(self.final == 1))]

    @property
    def final(self):
        return self._final

    @final.setter
    def final(self, value):
        self._final = np.add(self._final, value.copy())

    def get_boundaries(self):
        left_boundary = [(y, -1) for y in range(0, self.height)]
        right_boundary = [(y, self.width) for y in range(0, self.height)]
        bottom_boundary = [(self.height, x) for x in range(0, self.width)]
        return left_boundary + right_boundary + bottom_boundary

    def get_current(self, piece=None):
        if self.game_over:
            return self.redraw(game_over=True)
        if piece:
            prev_current = self.current.copy()
            self.current = np.zeros(shape=(self.height, self.width))
            p_obj = piece
            p_array = piece.position
            y, x = p_array.shape
            try:
                self.current[p_obj.cord_y:p_obj.cord_y + y,
                             p_obj.cord_x:p_obj.cord_x + x] = p_array
            except (NextPiece, GameOver):
                self.final = prev_current
            return render_current_screen(np.add(self.final, self.current))
        return render_current_screen(self.final)

    def redraw(self, game_over=False):
        self.final = self.current
        if game_over:
            self.game_over = True
            raise GameOver
        raise DeadEndError


def render_current_screen(board):
    board = np.char.mod('%d', board)
    board[board == '1'] = '*'
    board[board == '0'] = ' '
    np.set_printoptions(linewidth=200)
    return print(board)
