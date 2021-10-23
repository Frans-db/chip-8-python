from dataclasses import dataclass, field

@dataclass
class Keyboard:
  pressed: list[int] = field(default_factory=list)
  
  def key_down(self, key: int):
    if key not in self.pressed:
      self.pressed.append(key)

  def key_up(self, key: int):
    if key in self.pressed:
      self.pressed.remove(key)

  def is_pressed(self, key: int):
    return key in self.pressed