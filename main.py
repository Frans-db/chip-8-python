from cpu import CPU
import time
import cv2
import numpy as np
import utils

def main():
  rom_location = 'roms/Particle Demo [zeroZshadow, 2008].ch8'
  with open(rom_location, 'rb') as f:
    rom = f.read()
  # rom = [0x60, 0x00, 0x61, 0x00, 0xA0, 5, 0xD0, 0x15]

  cpu = CPU()
  cpu.load_rom(rom)
  while True:
    opcode, assembly = cpu.step()
    # print([cpu.registers[r].value for r in cpu.registers], cpu.PC.value, cpu.SP.value, cpu.I.value)
    if 'DRW' in assembly:
      cpu.display.prettyprint()
      dp = np.array(cpu.display.display, dtype='uint8') * 255
      cv2.imshow('test', dp)
      cv2.waitKey(1)

if __name__ == '__main__':
  main()