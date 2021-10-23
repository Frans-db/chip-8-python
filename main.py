from cpu import CPU
from memory import Memory

def main():
  memory = Memory()
  print(len(memory))
  for i,_ in enumerate(memory):
    memory[i] = i
  for i,value in enumerate(memory):
    print(f'{i}: {value}')

if __name__ == '__main__':
  main()