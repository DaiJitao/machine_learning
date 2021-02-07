

import numpy as np

class Demo(object):

    def __init__(self):
        self.name = 'lll'

    def __del__(self):
        print('即将被销毁')

    def fly(self):
        print("我会飞")

    def __str__(self):
        return "__str__::dai"

class MyDemo(Demo):

    def fly(self):
        print("MyDemo 会飞")

class DaiDemo(MyDemo):
    def fly(self):
        super().fly()
        print('DaiDemo---->')






if __name__ == '__main__':
    print(np.__doc__)
    demo = Demo()
    print(demo.name)
    demo.name = 'DAI'
    print(demo.name)
    print(demo.fly())
    print('--------')
    d = DaiDemo()
    print(d.fly())
    a = A()
    print(a.fly())
    # my = MyDemo()
    # print(my.fly())
    # print(my.name)