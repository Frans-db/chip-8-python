import unittest
from memory import Memory

from register import Register, Register16Bit
from stack import Stack

class TestRegister(unittest.TestCase):
  def setUp(self) -> None:
    self.r = Register('r')

  def test_set(self):
    self.r.value = 5
    self.assertEqual(self.r.value, 5)

  def test_set_overflow(self):
    self.r.value = 657
    self.assertEqual(self.r.value, 145)

class TestRegister16Bit(unittest.TestCase):
  def setUp(self) -> None:
    self.r = Register16Bit('r')

  def test_set(self):
    self.r.value = 5
    self.assertEqual(self.r.value, 5)

  def test_set_overflow_1(self):
    self.r.value = 2**16
    self.assertEqual(self.r.value, 0)

  def test_set_overflow_2(self):
    self.r.value = 2**16 + 145
    self.assertEqual(self.r.value, 145)

class TestMemory(unittest.TestCase):
  def setUp(self) -> None:
    self.memory = Memory()

  def test_set(self):
    for i,_ in enumerate(self.memory):
      self.memory[i] = 50
    for i,_ in enumerate(self.memory):
      self.assertEqual(self.memory[i], 50)

  def test_set_overflow(self):
    for i,_ in enumerate(self.memory):
      self.memory[i] = i
    for i,_ in enumerate(self.memory):
      self.assertEqual(self.memory[i], i & 0xFF)

class TestStack(unittest.TestCase):
  def setUp(self) -> None:
    self.stack = Stack()

  def test_set(self):
    for i,_ in enumerate(self.stack):
      self.stack[i] = 50
    for i,_ in enumerate(self.stack):
      self.assertEqual(self.stack[i], 50)

  def test_set_overflow_1(self):
    for i,_ in enumerate(self.stack):
      self.stack[i] = 2**16
    for i,_ in enumerate(self.stack):
      self.assertEqual(self.stack[i], 0)
    
  def test_set_overflow_2(self):
    for i,_ in enumerate(self.stack):
      self.stack[i] = 2**16 + i
    for i,_ in enumerate(self.stack):
      self.assertEqual(self.stack[i], i)

if __name__ == '__main__':
  unittest.main()