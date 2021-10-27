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