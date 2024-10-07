def qux():
    print('[mod4] qux()')


class Qux:
    pass


from .. import sub_pkg1
#print(sub_pkg1)

from ..sub_pkg1.mod1 import foo
#foo()