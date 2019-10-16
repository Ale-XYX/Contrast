#!/usr/bin/env python3

'''
// Contrast //

A puzzle-platformer about flipping the background, or something.

Code: Pygasm // Art: Keyghman 

Pyweek 25 (2018)
'''

import os
import sys
import tkinter
import tkinter.messagebox

# Check for required modules, if not, notify user.
# TODO: Reimplement the PIP self-install
try:
    import pygame
    import pytmx

except ModuleNotFoundError: 
    # The best part about making error screens
    # Is that TK doesnt know how to
    # (Without creating a Tk window, at least)

    ROOT = tkinter.Tk().withdraw()
    tkinter.messagebox.showerror(
        'Modules Not Found!',
        'Please install Pygame and/or PyTMX with Pip.'
    )

    sys.exit()

# Make this client script know about the 5 files in /src/
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))
import game # I DEFY YOU PEP MAN

if __name__ == '__main__':
    pygame.init()
    game.title(sys.argv)
    pygame.quit()

# :^)
