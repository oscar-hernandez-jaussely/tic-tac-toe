
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

