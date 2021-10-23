from dataclasses import dataclass

@dataclass
class Register:
  _name: str
  _value: int = int('00000000', 2)

  @property
  def name(self) -> str:
    return self._name

  @property
  def value(self) -> int:
    return self._value

  @value.setter
  def value(self, value) -> None:
    self._value = value & 0xFF

class Register16Bit(Register):
  @property
  def value(self) -> int:
    return self._value

  @value.setter
  def value(self, value) -> None:
    self._value = value & 0xFFFF

@dataclass
class FlagRegister(Register):
  _name: str = 'f'
  zero: bool = False
  subtract: bool = False
  half_carry: bool = False
  carry: bool = False

  @property
  def value(self) -> int:
    nibble = \
    ('1' if self.zero else '0') + \
    ('1' if self.subtract else '0') + \
    ('1' if self.half_carry else '0') + \
    ('1' if self.carry else '0')
    return (int(nibble, 2) << 4) | 0x00