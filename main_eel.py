import eel
from random import randint

from cpu import CPU

speed = 8

# read rom
rom_location = 'roms/Framed MK2 [GV Samways, 1980].ch8'
with open(rom_location, 'rb') as f:
  rom = f.read()

# create CPU and load rom
cpu = CPU()
cpu.load_rom(rom)

eel.init("web")

# Exposing the random_python function to javascript


@eel.expose
def random_python():
    print("Random function running")
    return randint(1, 100)


@eel.expose
def get_status():
    return 'success'


@eel.expose
def update_status(pressed):
    cpu.keyboard.pressed = pressed
    for _ in range(speed):
        cpu.step()
    return cpu.display.display


# Start the index.html file
eel.start("index.html")
