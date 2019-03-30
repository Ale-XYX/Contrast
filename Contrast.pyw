#!/usr/bin/env python3

import os
import sys
import tkinter
import tkinter.messagebox

try:
    import pygame
    import pytmx

except ModuleNotFoundError:
    ROOT = tkinter.Tk().withdraw()
    tkinter.messagebox.showerror(
        'Modules Not Found!',
        'Please install Pygame and/or PyTMX with Pip.'
    )

    sys.exit()

sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))
import game

if __name__ == '__main__':
    pygame.init()
    game.title()
    pygame.quit()

# :^)
