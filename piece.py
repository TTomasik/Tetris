import numpy as np
import random

from exceptions import GameOver, DeadEndError, DirectionError, WrongKeyError


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
    init_position = None

    def __init__(self, board):
        self.position = random.choice(PIECES)
        self.cord_x = random.randint(
            0, board.width - 1 - self.position.shape[1]
        )
        self.cord_y = 0
        self.board_width = board.width
        self.board_height = board.height
        if self.init_position is None:
            self.init_position =\
                self.get_coords(self.cord_x, self.cord_y, self.position)
            if any(coord in self.init_position for coord in board.taken_fields):
                board.game_over = True

    @staticmethod
    def get_coords(cord_x, cord_y, position):
        return [(y + cord_y, x + cord_x) for y, x in zip(*np.where(position == 1))]

    def set_new_position(self, action, taken_fields, allowed_actions, direction_error=False):
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
        if any(coord in self.get_coords(x, y, position) for coord in taken_fields):
            direction_error = True
            if len(allowed_actions) == 0:
                for y, x in self.get_coords(self.cord_x, self.cord_y, self.position):
                    if y <= 0:
                        raise GameOver
                raise DeadEndError
            action = allowed_actions.pop()
            return self.set_new_position(
                action, taken_fields, allowed_actions, direction_error
            )
        if direction_error:
            raise DirectionError
        return y, x, position

    def move(self, action, board):
        if action in self.allowed_actions:
            allowed_actions = self.allowed_actions.copy()
            taken_fields = board.taken_fields + board.get_boundaries()
            try:
                self.cord_y, self.cord_x, self.position =\
                    self.set_new_position(action, taken_fields, allowed_actions)
            except DeadEndError:
                board.redraw()
            except GameOver:
                board.redraw(game_over=True)
        else:
            raise WrongKeyError
