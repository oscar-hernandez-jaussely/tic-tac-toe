
import base
from base import *

import main
from main import *

import tictactoe_game
from tictactoe_game import *


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



