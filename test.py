from pathlib import Path

data = Path('/roms/BLINKY').read_bytes()
print(data)