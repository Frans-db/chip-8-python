import unittest

from register import Register

class TestRegister(unittest.TestCase):
  def setUp(self) -> None:
    self.r = Register('r')

  def test_set(self):
    self.r.value = 5
    self.assertEqual(self.r.value, 5)

  def test_set_overflow(self):
    self.r.value = 657
    self.assertEqual(self.r.value, 145)

if __name__ == '__main__':
  unittest.main()