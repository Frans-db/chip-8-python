def pp_opcode(opcode):
  print(convert_opcode(opcode))

def convert_opcode(opcode, include_opcode=True):
  identifier = opcode & 0xF000
  x = (opcode & 0x0F00) >> 8
  y = (opcode & 0x00F0) >> 4

  if identifier == 0x0000:
    if opcode & 0x0FFF == 0x00E0: # 00E0 - CLS 
      assembly = f'CLS'
    elif opcode & 0x0FFF == 0x00EE: # 00EE - RET
      assembly = f'RET'
  elif identifier == 0x1000: # 1nnn - JP ADDR
    assembly = f'JP {opcode & 0x0FFF}'
  elif identifier == 0x2000: # 2nnn - CALL addr
    assembly = f'CALL {opcode & 0x0FFF}'
  elif identifier == 0x3000: # 3xkk - SE Vx, byte
    assembly = f'SE V{x}, {opcode & 0x00FF}'
  elif identifier == 0x4000: # 4xkk - SNE Vx, byte
    assembly = f'SNE V{x}, {opcode & 0x00FF}'
  elif identifier == 0x5000: # 5xy0 - SE, Vx, Vy:
    assembly = f'SE, V{x}, V{y}'
  elif identifier == 0x6000: # 6xkk - LD Vx, byte
    assembly = f'LD V{x}, {opcode & 0x00FF}'
  elif identifier == 0x7000: # 7xkk - ADD Vx, byte:
    assembly = f'ADD V{x}, {opcode & 0x00FF}'
  elif identifier == 0x8000:
    if opcode & 0x000F == 0x0000: # 8xy0 - LD Vx, Vy
      assembly = f'LD V{x}, V{y}'
    elif opcode & 0x000F == 0x0001: # 8xy1 - OR Vx, Vy
      assembly = f'OR V{x}, V{y}'
    elif opcode & 0x000F == 0x0002: # 8xy2 - AND Vx, Vy
      assembly = f'AND V{x}, V{y}'
    elif opcode & 0x000F == 0x0003: # 8xy3 - XOR Vx, Vy
      assembly = f'XOR V{x}, V{y}'
    elif opcode & 0x000F == 0x0004: # 8xy4 - ADD Vx, Vy
      assembly = f'ADD V{x}, V{y}'
    elif opcode & 0x000F == 0x0005: # 8xy5 - SUB Vx, Vy
      assembly = f'SUB V{x}, V{y}'
    elif opcode & 0x000F == 0x0006: # 8xy6 - SHR Vx {, Vy}
      assembly = f'SHR V{x} ' + '{ ' + f'V{y}' + '}'
    elif opcode & 0x000F == 0x0007: # 8xy7 - SUBN Vx, Vy
      assembly = f'SUBN V{x}, V{y}'
    elif opcode & 0x000F == 0x000E: # 8xyE - SHL Vx {, Vy}
      assembly = f'SHL V{x} ' + '{ ' + f'V{y}' + '}'
  elif identifier == 0x9000: # 9xy0 - SNE Vx, Vy
    assembly = f'SNE V{x}, V{y}'
  elif identifier == 0xA000: # Annn - LD I, addr
    assembly = f'LD I, {opcode & 0x0FFF}'
  elif identifier == 0xB000: # Bnnn - JP v0, addr
    assembly = f'JP V0, {opcode & 0x0FFF}'
  elif identifier == 0xC000: # Cxkk - RND Vx, byte
    assembly = f'RND V{x}, {opcode & 0x0FFF}'
  elif identifier == 0xD000: # Dxyn - DRW Vx, Vy, nibble
    assembly = f'DRW V{x}, V{y}, {opcode & 0x000F}'
  elif identifier == 0xE000:
    if opcode & 0x009E: # Ex9E - SKP Vx
      assembly = f'SKP V{x}'
    elif opcode & 0x00A1: #Ex1A - SKNP Vx
      assembly = f'SKNP V{x}'
  elif identifier == 0xF000:
    if opcode & 0x00FF == 0x0007: # Fx07 - LD Vx, DT
      assembly = f'LD V{x}, DT'
    elif opcode & 0x00FF == 0x000A: # Fx0A - LD, Vx, K
      assembly = f'LD, V{x}, K'
    elif opcode & 0x00FF == 0x0015: # Fx15 - LD DT, Vx
      assembly = f'LD DT, V{x}'
    elif opcode & 0x00FF == 0x0018: # Fx18 - LD, ST, Vx
      assembly = f'LD ST, V{x}'
    elif opcode & 0x00FF == 0x001E: # Fx1E - ADD I, Vx
      assembly = f'ADD I, V{x}'
    elif opcode & 0x00FF == 0x0029: # Fx29 - LD F, Vx
      assembly = f'ADD F, V{x}'
    elif opcode & 0x00FF == 0x0033: # Fx33 - LD B, Vx
      assembly = f'LD B, V{x}'
    elif opcode & 0x00FF == 0x0055: # Fx55 - LD [I], Vx
      assembly = f'LD [I], V{x}'
    elif opcode & 0x00FF == 0x0065: # Fx65 - LD Vx, [I]
      assembly = f'LD V{x}, [i]'
  else:
    raise Exception('Opcode not implemented')
  
  if include_opcode:
    opcode_string = hex(opcode)[2:]
    while len(opcode_string) < 4:
      opcode_string = '0' + opcode_string
    assembly = f'{opcode_string.upper()} - {assembly}'
  return assembly