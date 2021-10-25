import cv2
import numpy as np
import keyboard

from cpu import CPU

import cProfile
import pstats
import time

conversions = {
  '0': 0x0,
  '1': 0x1,
  '2': 0x2,
  '3': 0x3,
  '4': 0x4,
  '5': 0x5,
  '6': 0x6,
  '7': 0x7,
  '8': 0x8,
  '9': 0x9,
  'a': 0xA,
  'b': 0xB,
  'c': 0xC,
  'd': 0xD,
  'e': 0xE,
  'f': 0xF,
}

cpu = CPU()

def on_press(event):
  cpu.keyboard.key_down(conversions[event.name])


def on_release(event):
  cpu.keyboard.key_up(conversions[event.name])

def main():
  # for key in conversions:
  #   keyboard.on_press_key(key, on_press)
  #   keyboard.on_release_key(key, on_release)


  rom_location = 'roms/Framed MK2 [GV Samways, 1980].ch8'
  with open(rom_location, 'rb') as f:
    rom = f.read()

  cpu.load_rom(rom)
  
  iteration = 0
  while iteration < 100_000:
    iteration += 1
    # time.sleep(0.01)
    draw = cpu.step()

    # display
    # if 'DRW' in assembly:
    #   scaling = 8
    #   scaled = []
    #   for row in cpu.display.display:
    #     new_row = []
    #     for value in row:
    #       for _ in range(scaling):
    #         new_row.append(value)
    #     for _ in range(scaling):
    #       scaled.append(new_row)
    #   dp = np.array(scaled, dtype='uint8') * 255
    #   cv2.imshow('test', dp)
    #   cv2.waitKey(1)

if __name__ == '__main__':
  with cProfile.Profile() as pr:
    main()
  stats = pstats.Stats(pr)
  stats.sort_stats(pstats.SortKey.TIME)
  stats.print_stats()
  stats.dump_stats(filename=f'profiling/{time.time()}.prof')