# Copyright (C) 2017 Fassio Blatter

class Singleton(type):
    """
    inherit: (StatefulClass,metaclass=Singleton)
    not suitable for StatefulClasses with custom new or init
    not suitable for StatefulClasses with their own type information
    """
    _instances = {}
    ## type.__call__ is type(), not type()() unlike object()()
    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton,cls).__call__(*args, **kwargs)
        return cls._instances[cls]
    ## Prohibited!
    # def __new__(cls, *args, **kwargs):
    #     print(str(cls)+"__new__")
    #     super(Singleton,cls).__new__(cls,*args, **kwargs)
    def __init__(cls, *args, **kwargs):
        super(Singleton,cls).__init__(*args, **kwargs)

class SingletonList(list,metaclass=Singleton):
    pass
import numpy
from numpy import ndarray
class SingletonNumpy(ndarray,metaclass=Singleton):
    def __call__(cls, *args, **kwargs):
        print("__call__ sub")

if __name__ == '__main__':
    print("__main__")
    test1 = SingletonList()
    test1.append("5")
    print(test1)
    if (len(test1)!=1):
        raise Exception("test1 assignment failed!")
    test2 = SingletonList()
    test2.append("7")
    print(test2)
    if (len(test2)!=2):
        raise Exception("test2 assignment failed!")
    if (len(test1)!=len(test2)):
        raise Exception("SingletonList instantiation test failed!")
    test3 = SingletonNumpy(shape=(1,),dtype=numpy.int16)
    test3[0]=77
    print(test3)
    if (len(test3)!=1):
        raise Exception("test3 assignment failed!")
    test4 = SingletonNumpy(shape=(1,),dtype=numpy.int16)
    test4 = numpy.append(test4,[88])
    print(test4)
    if (len(test4)!=2):
        raise Exception("test4 assignment failed!")
    if (len(test3)!=len(test4)-1):
        print(str(len(test3))+","+str(len(test4)))
        raise Exception("SingletonList instantiation test failed!")

