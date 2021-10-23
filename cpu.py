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
