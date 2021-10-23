from typing import Dict

from register import Register, Register16Bit
from memory import Memory
from stack import Stack

class CPU:
  registers: dict[str, Register] = {}

  I = Register16Bit('I')
  PC = Register16Bit('PC')
  SP = Register16Bit('SP')

  delay = Register('delay')
  sound = Register('sound')

  memory = Memory()
  stack = Stack()

  def __init__(self) -> None:
      for i in range(0, 16):
        self.registers[i] = Register(f'v{hex(i)[2:]}')

  def execute_opcode(self, opcode) -> None:
    identifier = opcode & 0xF000
    x = (opcode & 0x0F00) >> 8
    y = (opcode & 0x00F0) >> 4
    if identifier == 0x0000:
      if opcode & 0x0FFF == 0x00E0: # 00E0 - CLS 
        pass # TODO: Figure out display
      elif opcode & 0x0FFF == 0x00EE: # 00EE - RET
        self.PC.value = self.stack[self.SP.value]
        self.SP.value -= 1
    elif identifier == 0x1000: # 1nnn - JP ADDR
      self.PC.value = opcode & 0x0FFF
    elif identifier == 0x2000: # 2nnn - CALL addr
      self.SP.value += 1
      self.stack[self.SP.value] = self.PC
      self.PC = opcode & 0x0FFF
    elif identifier == 0x3000: # 3xkk - SE Vx, byte
      if self.registers[x].value == opcode & 0x00FF:
        self.PC += 2
    elif identifier == 0x4000: # 4xkk - SNE Vx, byte
      if self.registers[x].value != opcode & 0x00FF:
        self.PC += 2 
    elif identifier == 0x5000: # 5xy0 - SE, Vx, Vy:
      if self.registers[x].value == self.registers[y].value:
        self.PC += 2 
    elif identifier == 0x6000: # 6xkk - LD Vx, byte
      self.registers[x] = opcode & 0x00FF
    elif identifier == 0x7000: # 7xkk - ADD Vx, byte:
      self.registers[x] += opcode & 0x00FF
    elif identifier == 0x8000:
      if opcode & 0x000F == 0x0000: # 8xy0 - LD Vx, Vy
        self.registers[x] = self.registers[y]
      elif opcode & 0x000F == 0x0001: # 8xy1 - OR Vx, Vy
        self.registers[x] |= self.registers[y]
      elif opcode & 0x000F == 0x0002: # 8xy2 - AND Vx, Vy
        self.registers[x] &= self.registers[y]
      elif opcode & 0x000F == 0x0003: # 8xy3 - XOR Vx, Vy
        self.registers[x] ^= self.registers[y]
      elif opcode & 0x000F == 0x0004: # 8xy4 - ADD Vx, Vy
        result = self.registers[x] + self.registers[y]
        self.registers[0xF] = 0
        if result > 255:
          self.registers[0xF] = 1
        self.registers[x] = result
      elif opcode & 0x000F == 0x0005: # 8xy5 - SUB Vx, Vy
        self.registers[0xF] = 0
        if self.registers[x] > self.registers[y]:
          self.registers[0xF] = 1
        self.registers[x] -= self.registers[y]
      elif opcode & 0x000F == 0x0006: # 8xy6 - SHR Vx {, Vy}
        self.registers[0xF] = opcode & 0x01
        self.registers[x] >>= 1
      elif opcode & 0x000F == 0x0007: # 8xy7 - SUBN Vx, Vy
        self.registers[0xF] = 0
        if self.registers[y] > self.registers[x]:
          self.registers[0xF] = 1
        self.registers[y] -= self.registers[x]
      elif opcode & 0x000F == 0x000E: # 8xyE - SHL Vx {, Vy}
        self.registers[0xF] = self.registers[x] & 0x80
        self.registers[x] <= 1
    elif identifier == 0xA000: # 9xy0 - SNE Vx, Vy
      pass