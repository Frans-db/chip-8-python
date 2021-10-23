import unittest
from cpu import CPU
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

class TestCPU(unittest.TestCase):
  def setUp(self) -> None:
    self.cpu = CPU()
  
  # 00E0 - CLS
  def test_00E0_1(self):
    self.cpu.execute_opcode(0x00E0)
    for row in self.cpu.display.display:
      for value in row:
        self.assertEqual(value, 0)

  # 2nnn - CALL addr
  # 00EE - RET
  def test_call_ret(self):
    self.cpu.execute_opcode(0x2123)
    self.assertEqual(self.cpu.PC.value, 0x0125)
    self.assertEqual(self.cpu.SP.value, 1)
    self.assertEqual(self.cpu.stack.stack[1], 0x200)

    self.cpu.execute_opcode(0x00EE)
    self.assertEqual(self.cpu.PC.value, 0x0202)
    self.assertEqual(self.cpu.SP.value, 0)

  # 1nnn - JP ADDR
  def test_1nnn(self):
    self.cpu.execute_opcode(0x1111)
    self.assertEqual(self.cpu.PC.value, 0x0113)
    self.cpu.execute_opcode(0x1200)
    self.assertEqual(self.cpu.PC.value, 0x0202)

  def test_7xkk_1(self): # # 7xkk - ADD Vx, byte
    self.cpu.execute_opcode(0x7021)
    self.assertEqual(self.cpu.registers[0].value, 0x21)

  def test_7xkk_2(self): # # 7xkk - ADD Vx, byte
    self.cpu.execute_opcode(0x7021)
    self.cpu.execute_opcode(0x7052)
    self.cpu.execute_opcode(0x7129)
    self.assertEqual(self.cpu.registers[0].value, 0x73)
    self.assertEqual(self.cpu.registers[1].value, 0x29)

  def test_7xkk_3(self): # # 7xkk - ADD Vx, byte
    self.cpu.execute_opcode(0x70FF)
    self.cpu.execute_opcode(0x7002)
    self.assertEqual(self.cpu.registers[0].value, 0x01)


if __name__ == '__main__':
  unittest.main()