
import base
from base import *

import tictactie_board
from tictactie_board import *

import tictactoe_game
from tictactoe_game import *


def main():
    game = TicTacToeGame()
    board = TicTacToeBoard(game)

    largeur_fenetre = 500
    hauteur_fenetre = 500

    largeur_ecran = int(board.winfo_screenwidth())
    hauteur_ecran = int(board.winfo_screenheight())

    position_fenetre_largeur = (largeur_ecran // 2) - (largeur_fenetre // 2)
    position_fenetre_hauteur = (hauteur_ecran // 2) - (hauteur_fenetre // 2)

    board.geometry(f"{largeur_fenetre}x{hauteur_fenetre}+{position_fenetre_largeur}+{position_fenetre_hauteur}")

    board.configure(background=bg_color)

    board.mainloop()

if __name__ == "__main__":
    main()

