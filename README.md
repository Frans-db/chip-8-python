# python-chip-8
Python CHIP-8 emulator created following instructions from http://devernay.free.fr/hacks/chip8/C8TECH10.HTM (with help from https://www.freecodecamp.org/news/creating-your-very-own-chip-8-emulator/)

## Versions
Python 3.9.6

## Structure
TODO: Create proper package structure

The emulation functionality is all handled in the CPU class in cpu.py. This file runs without any extra packages.

For displaying and I/O extra packages are needed. I made 2 examples (main.py and main_eel.py)

**main.py** used the python-opencv (cv2) and keyboard packages to handle I/O

**main_eel.py** used eel to create a web interface to handle I/O

