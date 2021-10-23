from cpu import CPU
import time
import cv2
import numpy as np
import utils

def main():
  # arr = []
  # for y in range(32):
  #   row = []
  #   for x in range(64):
  #     row.append(0)
  #   arr.append(row)
  # # arr = [[0] * 64] * 32
  # arr[0][1] = 1
  # print(arr)
  rom_location = 'roms/Chip8 emulator Logo [Garstyciuks].ch8'
  with open(rom_location, 'rb') as f:
    rom = f.read()

  cpu = CPU()
  cpu.load_rom(rom)
  while True:
    opcode, assembly = cpu.step()
    if 'DRW' in assembly:
      cpu.display.prettyprint()
      dp = np.array(cpu.display.display, dtype='uint8') * 255
      cv2.imshow('test', dp)
      cv2.waitKey(1)


if __name__ == '__main__':
  main()