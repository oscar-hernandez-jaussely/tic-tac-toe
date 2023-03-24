
import tkinter as tk
from itertools import cycle
from tkinter import font
from typing import NamedTuple

bg_color = "#1c4986"

class Player(NamedTuple): 
    label: str
    color: str

class Move(NamedTuple): 
    row: int
    col: int
    label: str = ""

BOARD_SIZE = 3
DEFAULT_PLAYERS = (
    Player(label="X", color="blue"),
    Player(label="O", color="green"),
)

class TicTacToeGame:
    def __init__(self, players=DEFAULT_PLAYERS, board_size=BOARD_SIZE):
        self._players = cycle(players)
        self.board_size = board_size
        self.current_player = next(self._players)
        self.winner_combo = []
        self._current_moves = []
        self._has_winner = False
        self._winning_combos = []
        self._setup_board()
        self.alt_color = "white"

    def _setup_board(self):
        self._current_moves = [
            [Move(row, col) for col in range(self.board_size)]
            for row in range(self.board_size)
        ]
        self._winning_combos = self._get_winning_combos()

    def _get_winning_combos(self):
        rows = [
            [(move.row, move.col) for move in row]
            for row in self._current_moves
        ]
        columns = [list(col) for col in zip(*rows)]
        first_diagonal = [row[i] for i, row in enumerate(rows)]
        second_diagonal = [col[j] for j, col in enumerate(reversed(columns))]
        return rows + columns + [first_diagonal, second_diagonal]
    
    def is_valid_move(self, move):
        row, col = move.row, move.col
        move_was_not_played = self._current_moves[row][col].label == ""
        no_winner = not self._has_winner
        return no_winner and move_was_not_played

    def process_move(self, move):
        row, col = move.row, move.col
        self._current_moves[row][col] = move
        for combo in self._winning_combos:
            results = set(
                self._current_moves[n][m].label
                for n, m in combo
            )
            is_win = (len(results) == 1) and ("" not in results)
            if is_win:
                self._has_winner = True
                self.winner_combo = combo
                break

    def has_winner(self):
        return self._has_winner
    

    def is_tied(self):
        no_winner = not self._has_winner
        played_moves = (
            move.label for row in self._current_moves for move in row
        )
        return no_winner and all(played_moves)
    
    def toggle_player(self):
        self.current_player = next(self._players)




class TicTacToeBoard(tk.Tk):
    def __init__(self, game):
        super().__init__()
        self.title("TicTacToe")
        self._cells ={}
        self._game = game
        self._create_board_display()
        self._create_board_grid()   

    def _create_board_display(self):
        display_frame = tk.Frame(master=self)
        display_frame.pack(fill=tk.X)
        self.display = tk.Label(
            master=display_frame,
            text="Welcome to TicTacToe game ! \n Ready ? \n",
            font=font.Font(size=18, weight="bold"),
            background=bg_color,
            foreground="white"
        )
        self.display.pack(fill="both")


    def _create_board_grid(self):
        grid_frame = tk.Frame(master=self)
        grid_frame.pack()
        for row in range(self._game.board_size):
            self.rowconfigure(row, weight=1, minsize=50)
            self.columnconfigure(row, weight=1, minsize=75)
            for col in range(self._game.board_size):
                button = tk.Button(
                    master=grid_frame,
                    text="",
                    font=font.Font(size=36, weight="bold"),
                    fg="black",
                    width=3,
                    height=1,
                )
                self._cells[button] = (row, col)
                button.bind("<ButtonPress-1>", self.play)
                button.grid(
                    row=row,
                    column=col,
                    padx=5,
                    pady=5,
                    sticky="nsew"
                )

    def play(self, event):
        clicked_btn = event.widget
        row, col = self._cells[clicked_btn]
        move = Move(row, col, self._game.current_player.label)
        if self._game.is_valid_move(move):
            self._update_button(clicked_btn)
            self._game.process_move(move)
            if self._game.is_tied():
                self._update_display(msg="\nTied game ! \n", color="red")
            elif self._game.has_winner():
                self._highlight_cells()
                msg = f'\nPlayer "{self._game.current_player.label}" won ! \n'
                color = self._game.alt_color
                self._update_display(msg, color)
            else:
                self._game.toggle_player()
                msg = f"\n{self._game.current_player.label}'s turn \n"
                self._update_display(msg)

    def _update_button(self, clicked_btn):
        clicked_btn.config(text=self._game.current_player.label)
        clicked_btn.config(fg=self._game.current_player.color)

    def _update_display(self, msg, color="black"):
        self.display["text"] = msg
        self.display["fg"] = color

    def _highlight_cells(self):
        for button, coordinates in self._cells.items():
            if coordinates in self._game.winner_combo:
                button.config(highlightbackground="red")

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

