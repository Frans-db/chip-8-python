import random
import math

from .register import Register, Register16Bit
from .memory import Memory
from .stack import Stack
from .display import Display
from .virtualkeyboard import Keyboard
from .utils import convert_opcode

class CPU:
  registers: dict[str, Register] = {}
  I = Register16Bit('I')
  PC = Register16Bit('PC')
  SP = Register16Bit('SP')

  DT = Register('delay')
  ST = Register('sound')

  memory = Memory()
  stack = Stack()

  display = Display()
  keyboard = Keyboard()

  def __init__(self) -> None:
    for i in range(0, 16):
      self.registers[i] = Register(f'v{hex(i)[2:]}')
    self.PC.value = 0x200
    self.flag = self.registers[0xF]

  def step(self):
    if self.DT.value > 0:
      self.DT.value -= 1
    if self.ST.value > 0:
      self.ST.value -= 1
    opcode = self.memory[self.PC.value] << 8 | self.memory[self.PC.value + 1]
    return self.execute_opcode(opcode)

  def load_rom(self, rom):
    for i,value in enumerate(rom):
      self.memory[0x200 + i] = value

  def execute_opcode(self, opcode) -> None:
    # print(f'{self.PC.value} - {convert_opcode(opcode)}')
    self.PC.value += 2

    start = (opcode & 0xF000) >> 12
    end = (opcode & 0x000F)
    x = (opcode & 0x0F00) >> 8
    y = (opcode & 0x00F0) >> 4
    nnn = (opcode & 0x0FFF)
    kk = (opcode & 0x00FF)
    rx = self.registers[x]
    ry = self.registers[y]


    if start == 0x0:
      if nnn == 0x0E0: # 00E0 - CLS 
        self.display.clear()
        return True
      elif nnn == 0x0EE: # 00EE - RET
        self.SP.value -= 1
        self.PC.value = self.stack[self.SP.value]
    elif start == 0x1: # 1nnn - JP ADDR
      self.PC.value = nnn
    elif start == 0x2: # 2nnn - CALL addr
      self.stack[self.SP.value] = self.PC.value
      self.PC.value = nnn
      self.SP.value += 1
    elif start == 0x3: # 3xkk - SE Vx, byte
      if rx.value == kk:
        self.PC.value += 2
    elif start == 0x4: # 4xkk - SNE Vx, byte
      if rx.value != kk:
        self.PC.value += 2 
    elif start == 0x5: # 5xy0 - SE, Vx, Vy:
      if rx.value == ry.value:
        self.PC.value += 2 
    elif start == 0x6: # 6xkk - LD Vx, byte
      rx.value = kk
    elif start == 0x7: # 7xkk - ADD Vx, byte:
      rx.value += kk
    elif start == 0x8:
      if end == 0x0: # 8xy0 - LD Vx, Vy
        rx.value = ry.value
      elif end == 0x1: # 8xy1 - OR Vx, Vy
        rx.value |= ry.value
      elif end == 0x2: # 8xy2 - AND Vx, Vy
        rx.value &= ry.value
      elif end == 0x3: # 8xy3 - XOR Vx, Vy
        rx.value ^= ry.value
      elif end == 0x4: # 8xy4 - ADD Vx, Vy
        result = rx.value + ry.value
        self.flag.value = 0
        if result > 255:
          self.flag.value = 1
        rx.value = result
      elif end == 0x5: # 8xy5 - SUB Vx, Vy
        self.flag.value = 0
        if rx.value > ry.value:
          self.flag.value = 1
        rx.value -= ry.value
      elif end == 0x6: # 8xy6 - SHR Vx {, Vy}
        self.flag.value = rx.value & 0x001
        rx.value >>= 1
      elif end == 0x7: # 8xy7 - SUBN Vx, Vy
        self.flag.value = 0
        if ry.value > rx.value:
          self.flag.value = 1
        rx.value = (ry.value - rx.value)
      elif end == 0xE: # 8xyE - SHL Vx {, Vy}
        self.flag.value = rx.value & 0x80
        rx.value <<= 1
    elif start == 0x9: # 9xy0 - SNE Vx, Vy
      if rx.value != ry.value:
        self.PC.value += 2 
    elif start == 0xA: # Annn - LD I, addr
      self.I.value = nnn
    elif start == 0xB: # Bnnn - JP v0, addr
      self.PC.value = nnn + self.registers[0].value
    elif start == 0xC: # Cxkk - RND Vx, byte
      rx.value = random.randint(0, 255) & kk
    elif start == 0xD: # Dxyn - DRW Vx, Vy, nibble
      self.flag.value = 0
      for i in range(end):
        for j,value in enumerate(bin(self.memory[self.I.value + i])[2:].zfill(8)):
          if int(value) < 1:
            continue
          if self.display.draw_pixel(rx.value+j, ry.value+i):
            self.flag.value = 1
      return True
    elif start == 0xE:
      if kk == 0x9E: # Ex9E - SKP Vx
        if self.keyboard.is_pressed(rx.value):
          self.PC.value += 2
      elif kk == 0xA1: #ExA1 - SKNP Vx
        if not self.keyboard.is_pressed(rx.value):
          self.PC.value += 2
    elif start == 0xF:
      if kk == 0x07: # Fx07 - LD Vx, DT
        rx.value = self.DT.value
      elif kk == 0x0A: # Fx0A - LD, Vx, K
        while True:
          if len(self.keyboard.pressed) > 0:
            rx.value = self.keyboard.pressed[0]
            break
      elif kk == 0x15: # Fx15 - LD DT, Vx
        self.DT.value = rx.value
      elif kk == 0x18: # Fx18 - LD, ST, Vx
        self.ST.value = rx.value
      elif kk == 0x1E: # Fx1E - ADD I, Vx
        self.I.value += rx.value
      elif kk == 0x29: # Fx29 - LD F, Vx
        self.I.value = rx.value * 5
      elif kk == 0x33: # Fx33 - LD B, Vx
        self.memory[self.I.value    ] = math.floor(rx.value / 100)
        self.memory[self.I.value + 1] = math.floor((rx.value % 100) / 10)
        self.memory[self.I.value + 2] = math.floor(rx.value % 10)
      elif kk == 0x55: # Fx55 - LD [I], Vx
        for i in range(x+1):
          self.memory[self.I.value + i] = self.registers[i].value
      elif kk == 0x65: # Fx65 - LD Vx, [I]
        for i in range(x+1):
          self.registers[i].value = self.memory[self.I.value + i]
    else:
      raise Exception('Opcode not implemented')
    return False
