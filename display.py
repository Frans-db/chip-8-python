class Display:
  def __init__(self, width=64, height=32) -> None:
    self.width = width
    self.height = height
    self.display = []
    for y in range(self.height):
      row = []
      for x in range(self.width):
        row.append(0)
      self.display.append(row)

  def clear(self):
    for y in range(self.height):
      for x in range(self.width):
        self.display[y][x] = 0

  def draw_pixel(self, x, y):
    new_x = x % self.width
    new_y = y % self.height
    if new_x < 0 or new_y < 0:
      raise Exception('draw outside bounds')
    collision = self.display[new_y][new_x] == 1
    self.display[new_y][new_x] = self.display[new_y][new_x] ^ 1
    return collision

  def prettyprint(self):
    table = ''
    for row in self.display:
      r = ''
      for value in row:
        r += f'{value} '
      table += f'{r[:-1]}\n'
    print(table)