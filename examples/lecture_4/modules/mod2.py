s = "If Comrade Napoleon says it, it must be right."
a = [100, 200, 300]


def foo(arg):
    print(f'arg = {arg}')


class Foo:
    def __init__(self):
        self.x = 42


print(s)
print(a)
foo('quux')
x = Foo()
print(x)