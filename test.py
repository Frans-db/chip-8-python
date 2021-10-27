class Test:
    i: int = 0

    def __get__(self):
        return self.i

    def __set__(self, value):
        self.i = value

t = Test()
t = 3
print(t)
