from dataclasses import dataclass

@dataclass
class uint8:
  _value: int

  @property
  def value(self):
    return self._value

  @value.setter
  def value(self, value):
    self.value = value & 0xFF

@dataclass
class uint16:
  _value: int

  @property
  def value(self):
    return self._value

  @value.setter
  def value(self, value):
    self.value = value & 0xFFFF