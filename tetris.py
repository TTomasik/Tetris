import numpy as np
import random


class DirectionError(Exception):
    pass


class DeadEndError(Exception):
    pass


class KeyError(Exception):
    pass


class GameOver(Exception):
    pass


PIECES = [
    np.array([[1, 1, 1, 1]]),
    np.array([[1, 0],
              [1, 0],
              [1, 1]]),
    np.array([[0, 1],
              [0, 1],
              [1, 1]]),
    np.array([[1, 1],
              [1, 1]]),
    np.array([[0, 1],
              [1, 1],
              [1, 0]])
]


class Piece:

    allowed_actions = ['w', 's', 'a', 'd']
    reload_board = False

    def __init__(self, board_width, board_height):
        self.position = random.choice(PIECES)
        self.cord_x = random.randint(
            0, board_width - 1 - self.position.shape[1]
        )
        self.cord_y = 0
        self.board_width = board_width
        self.board_height = board_height

    def get_next_coords(self, cord_x, cord_y, position):
        return [(y + cord_y, x + cord_x) for y, x in zip(*np.where(position == 1))]

    def get_boundaries(self):
        left_boundary = [(y, -1) for y in range(0, self.board_height)]
        right_boundary = [(y, self.board_width) for y in range(0, self.board_height)]
        bottom_boundary = [(self.board_height, x) for x in range(0, self.board_width)]
        return left_boundary + right_boundary + bottom_boundary

    def check_if_possible(self, action, taken_fields, allowed_actions, direction_error=False):
        x = self.cord_x
        y = self.cord_y + 1
        position = self.position.copy()
        if action == 'w':
            position = np.rot90(position)
        elif action == 's':
            position = np.rot90(position, -1)
        elif action == 'a':
            x -= 1
        elif action == 'd':
            x += 1
        if any(coord in self.get_next_coords(x, y, position) for coord in taken_fields):
            direction_error = True
            if len(allowed_actions) == 0:
                for y, x in self.get_next_coords(self.cord_x, self.cord_y, self.position):
                    if y <= 0:
                        raise GameOver
                raise DeadEndError
            action = allowed_actions.pop()
            return self.check_if_possible(action, taken_fields, allowed_actions, direction_error)
        if direction_error:
            raise DirectionError
        return y, x, position

    def do_action(self, action, board):
        if action in self.allowed_actions:
            allowed_actions = self.allowed_actions.copy()
            taken_fields = board.taken_fields + self.get_boundaries()
            try:
                self.cord_y, self.cord_x, self.position =\
                    self.check_if_possible(action, taken_fields, allowed_actions)
            except DeadEndError as exc:
                board.refresh()
                raise exc
            except GameOver:
                board.game_over = True
                board.refresh()
        else:
            raise KeyError


class Board:

    height = 20
    width = 20
    game_over = False

    _final = np.zeros(shape=(20, 20))

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

    def get_current(self, piece=None):
        if self.game_over:
            return 'GAME OVER'
        if piece:
            previous_current = self.current.copy()
            self.current = np.zeros(shape=(20, 20))
            p_obj = piece
            p_array = piece.position
            y, x = p_array.shape
            try:
                self.current[p_obj.cord_y + y - 1]
                self.current[p_obj.cord_y:p_obj.cord_y + y, p_obj.cord_x:p_obj.cord_x + x] = p_array
            except (IndexError, ValueError) as exc:
                self.final = previous_current
                raise exc
            return get_current_screen(np.add(self.final, self.current))
        return get_current_screen(self.final)

    def refresh(self):
        self.final = self.current
        raise ValueError


def get_current_screen(board):
    board = np.char.mod('%d', board)
    board[board == '1'] = '*'
    board[board == '0'] = ' '
    np.set_printoptions(linewidth=200)
    return print(board)


def game():
    board = Board()
    piece = Piece(board.width, board.height)
    while True:
        try:
            board.get_current(piece)
            next_move = input('Whats your move?')
            try:
                piece.do_action(next_move.lower(), board)
            except KeyError:
                print("""
                Please provide correct action key:\n
                a - move piece left\n
                d - move piece right\n
                s - rotate piece clockwise\n
                w - rotate piece counter clockwise\n
                """)
                continue
            except DirectionError:
                print('\nCannot move piece in this direction.')
                continue
            except DeadEndError:
                piece = Piece(board.width, board.height)
        except (ValueError, IndexError):
            piece = Piece(board.width, board.height)


if __name__ == '__main__':
    game()
