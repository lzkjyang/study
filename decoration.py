from functools import wraps
from random import random

def  SaveToObjcet(a_func):
    @wraps(a_func)
    def wrapTheFunction():
        print("Save to iter")
        yield a_func()
        print ("\nfinish work")
    return wrapTheFunction

@SaveToObjcet
def readrandint():
    res = []
    for x in range(1,1000):
        res.append(random())
    return res


if __name__ == '__main__':
    for x in readrandint():
        print(x,end=' ')
