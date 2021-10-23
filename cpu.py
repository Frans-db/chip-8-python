import random

from register import Register, Register16Bit
from memory import Memory
from stack import Stack

class CPU:
  registers: dict[str, Register] = {}

  I = Register16Bit('I')
  PC = Register16Bit('PC')
  SP = Register16Bit('SP')

  DT = Register('delay')
  ST = Register('sound')

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
        result = self.registers[x].value + self.registers[y]
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
        self.registers[x].value <= 1
    elif identifier == 0x9000: # 9xy0 - SNE Vx, Vy
      if self.registers[x].value != self.registers[y].value:
        self.PC.value += 2 
    elif identifier == 0xA000: # Annn - LD I, addr
      self.I.value = opcode & 0x0FFF
    elif identifier == 0xB000: # Bnnn - JP v0, addr
      self.PC.value = (opcode & 0xFFF) + self.registers[0].value
    elif identifier == 0xC000: # Cxkk - RND Vx, byte
      self.registers[x].__init__ = random.randint(0, 255)
    elif identifier == 0xD000: # Dxyn - DRW Vx, Vy, nibble
      pass # TODO: Figure out display
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
        pass # TODO: Figure out sprites
      elif opcode & 0x00FF == 0x0033: # Fx33 - LD B, Vx
        pass # TODO
      elif opcode & 0x00FF == 0x0055: # Fx55 - LD [I], Vx
        pass # TODO
      elif opcode & 0x00FF == 0x0065: # Fx65 - LD Vx, [I]
        pass # TODO