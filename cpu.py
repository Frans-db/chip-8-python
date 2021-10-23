import random
import math

from register import Register, Register16Bit
from memory import Memory
from stack import Stack

from display import Display

import utils

class CPU:
  def __init__(self) -> None:
    self.registers: dict[str, Register] = {}
    self.I = Register16Bit('I')
    self.PC = Register16Bit('PC')
    self.SP = Register16Bit('SP')

    self.DT = Register('delay')
    self.ST = Register('sound')

    self.memory = Memory()
    self.stack = Stack()

    self.display = Display()

    for i in range(0, 16):
      self.registers[i] = Register(f'v{hex(i)[2:]}')
    self.PC.value = 0x200

  def step(self):
    opcode = self.memory[self.PC.value] << 8 | self.memory[self.PC.value + 1]
    # utils.pp_opcode(opcode)
    self.execute_opcode(opcode)
    self.PC.value += 2
    return opcode, utils.convert_opcode(opcode, include_opcode=False)

  def load_rom(self, rom):
    for i,value in enumerate(rom):
      self.memory[0x200 + i] = value

  def execute_opcode(self, opcode) -> None:
    print(f'{self.PC.value} - {utils.convert_opcode(opcode)}')
    identifier = opcode & 0xF000
    x = (opcode & 0x0F00) >> 8
    y = (opcode & 0x00F0) >> 4
    if identifier == 0x0000:
      if opcode & 0x0FFF == 0x00E0: # 00E0 - CLS 
        self.display.clear()
      elif opcode & 0x0FFF == 0x00EE: # 00EE - RET
        self.PC.value = self.stack[self.SP.value]
        self.SP.value -= 1
    elif identifier == 0x1000: # 1nnn - JP ADDR
      self.PC.value = opcode & 0x0FFF
    elif identifier == 0x2000: # 2nnn - CALL addr
      self.SP.value += 1
      self.stack[self.SP.value] = self.PC.value
      self.PC.value = opcode & 0x0FFF
    elif identifier == 0x3000: # 3xkk - SE Vx, byte
      if self.registers[x].value == opcode & 0x00FF:
        self.PC.value += 2
    elif identifier == 0x4000: # 4xkk - SNE Vx, byte
      if self.registers[x].value != opcode & 0x00FF:
        self.PC.value += 2 
    elif identifier == 0x5000: # 5xy0 - SE, Vx, Vy:
      if self.registers[x].value == self.registers[y].value:
        self.PC.value += 2 
    elif identifier == 0x6000: # 6xkk - LD Vx, byte
      self.registers[x].value = opcode & 0x00FF
    elif identifier == 0x7000: # 7xkk - ADD Vx, byte:
      self.registers[x].value += opcode & 0x00FF
    elif identifier == 0x8000:
      if opcode & 0x000F == 0x0000: # 8xy0 - LD Vx, Vy
        self.registers[x].value = self.registers[y].value
      elif opcode & 0x000F == 0x0001: # 8xy1 - OR Vx, Vy
        self.registers[x].value |= self.registers[y].value
      elif opcode & 0x000F == 0x0002: # 8xy2 - AND Vx, Vy
        self.registers[x].value &= self.registers[y].value
      elif opcode & 0x000F == 0x0003: # 8xy3 - XOR Vx, Vy
        self.registers[x].value ^= self.registers[y].value
      elif opcode & 0x000F == 0x0004: # 8xy4 - ADD Vx, Vy
        result = self.registers[x].value + self.registers[y].value
        self.registers[0xF].value = 0
        if result > 255:
          self.registers[0xF].value = 1
        self.registers[x].value = result
      elif opcode & 0x000F == 0x0005: # 8xy5 - SUB Vx, Vy
        self.registers[0xF].value = 0
        if self.registers[x].value > self.registers[y].value:
          self.registers[0xF].value = 1
        self.registers[x].value -= self.registers[y].value
      elif opcode & 0x000F == 0x0006: # 8xy6 - SHR Vx {, Vy}
        self.registers[0xF].value = opcode & 0x01
        self.registers[x].value >>= 1
      elif opcode & 0x000F == 0x0007: # 8xy7 - SUBN Vx, Vy
        self.registers[0xF].value = 0
        if self.registers[y].value > self.registers[x].value:
          self.registers[0xF].value = 1
        self.registers[y].value -= self.registers[x].value
      elif opcode & 0x000F == 0x000E: # 8xyE - SHL Vx {, Vy}
        self.registers[0xF].value = self.registers[x].value & 0x80
        self.registers[x].value <<= 1
    elif identifier == 0x9000: # 9xy0 - SNE Vx, Vy
      if self.registers[x].value != self.registers[y].value:
        self.PC.value += 2 
    elif identifier == 0xA000: # Annn - LD I, addr
      self.I.value = opcode & 0x0FFF
    elif identifier == 0xB000: # Bnnn - JP v0, addr
      self.PC.value = (opcode & 0xFFF) + self.registers[0].value
    elif identifier == 0xC000: # Cxkk - RND Vx, byte
      self.registers[x].value = random.randint(0, 255) & (opcode & 0x00FF)
    elif identifier == 0xD000: # Dxyn - DRW Vx, Vy, nibble
      sprite = ''
      for i in range(opcode & 0x000F):
        row = ''
        for j,value in enumerate(bin(self.memory[self.I.value + i])[2:].zfill(8)):
          row += f'{value} '
          if self.display.draw_pixel(self.registers[x].value+j, self.registers[y].value+i, int(value)):
            self.registers[0xF].value = 1
        sprite += f'{row[:-1]}\n'
      print()
      print(self.I.value, self.registers[x].value, self.registers[y].value)
      print(sprite)
    elif identifier == 0xE000:
      if opcode & 0x009E: # Ex9E - SKP Vx
        pass # TODO: Figure out keyboard input
      elif opcode & 0x00A1: #Ex1A - SKNP Vx
        pass # TODO: Figure out keyboard input
    elif identifier == 0xF000:
      if opcode & 0x00FF == 0x0007: # Fx07 - LD Vx, DT
        self.registers[x].value = self.DT.value
      elif opcode & 0x00FF == 0x000A: # Fx0A - LD, Vx, K
        pass # TODO: Figure out keyboard
      elif opcode & 0x00FF == 0x0015: # Fx15 - LD DT, Vx
        self.DT.value = self.registers[x].value
      elif opcode & 0x00FF == 0x0018: # Fx18 - LD, ST, Vx
        self.ST.value = self.registers[x].value
      elif opcode & 0x00FF == 0x001E: # Fx1E - ADD I, Vx
        self.I.value += self.registers[x].value
      elif opcode & 0x00FF == 0x0029: # Fx29 - LD F, Vx
        self.I.value = self.registers[x].value * 5
      elif opcode & 0x00FF == 0x0033: # Fx33 - LD B, Vx
        value = self.registers[x].value
        self.memory[self.I.value    ] = math.floor(value / 100)
        self.memory[self.I.value + 1] = math.floor((value % 100) / 10)
        self.memory[self.I.value + 2] = math.floor(value % 10)
      elif opcode & 0x00FF == 0x0055: # Fx55 - LD [I], Vx
        for i in range(16):
          self.memory[self.I.value + i] = self.registers[i].value
      elif opcode & 0x00FF == 0x0065: # Fx65 - LD Vx, [I]
        for i in range(16):
          self.registers[i].value = self.memory[self.I.value + i]
    else:
      raise Exception('Opcode not implemented')