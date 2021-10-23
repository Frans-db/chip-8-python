from typing import Dict
from register import Register, Register16Bit

class CPU:
  registers: dict[str, Register] = {}

  I = Register16Bit('I')
  PC = Register16Bit('PC')
  SP = Register16Bit('SP')

  delay = Register('delay')
  sound = Register('sound')

  def __init__(self) -> None:
      for i in '0123456789ABCDEF':
        self.registers[f'v{i}'] = Register(f'v{i}')

  def execute_opcode(self, opcode) -> None:
    identifier = opcode & 0xF000
    if identifier == 0x0000:
      if opcode & 0x0FFF == 0x00E0: #   00E0 - CLS 
        pass # TODO: Figure out display
      elif opcode & 0x0FFF == 0x00EE: # 00EE - RET
        # self.PC.value = self
        self.SP.value -= 1
    elif identifier == 0x1000: #        1nnn - JP ADDR
      address = opcode & 0x0FFF
      self.PC.value = address
    