from cpu import CPU
import time
import cv2
import numpy as np
import utils

def main():
  rom_location = 'roms/Framed MK2 [GV Samways, 1980].ch8'
  with open(rom_location, 'rb') as f:
    rom = f.read()

  cpu = CPU()
  cpu.load_rom(rom)
  while True:
    opcode, assembly = cpu.step()
    # print([cpu.registers[r].value for r in cpu.registers], cpu.PC.value, cpu.SP.value, cpu.I.value)
    if 'DRW' in assembly:
      scaling = 8
      scaled = []
      for row in cpu.display.display:
        new_row = []
        for value in row:
          for _ in range(scaling):
            new_row.append(value)
        for _ in range(scaling):
          scaled.append(new_row)
      dp = np.array(scaled, dtype='uint8') * 255
      cv2.imshow('test', dp)
      cv2.waitKey(1)

if __name__ == '__main__':
  main()