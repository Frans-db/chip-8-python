class Stack:
  def __init__(self, size = 16) -> None:
      self.stack = [0] * size
  
  def __getitem__(self, key):
    return self.stack[key]

  def __setitem__(self, key, value):
    self.stack[key] = value & 0xFFFF