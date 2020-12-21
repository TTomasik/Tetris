from board import Board
from piece import Piece
from exceptions import WrongKeyError, DirectionError, NextPiece, DeadEndError, GameOver


def game():
    board = Board()
    piece = Piece(board)
    while True:
        try:
            board.get_current(piece)
            next_move = input('Whats your move?')
            piece.move(next_move.lower(), board)
        except WrongKeyError:
            print("""
            Please provide correct action key:\n
            a - move piece left\n
            d - move piece right\n
            s - rotate piece clockwise\n
            w - rotate piece counter clockwise\n
            """)
        except DirectionError:
            print('\nCannot move piece in this direction.')
        except (NextPiece, DeadEndError):
            piece = Piece(board)
        except GameOver:
            return print('GAME OVER')


if __name__ == '__main__':
    game()
