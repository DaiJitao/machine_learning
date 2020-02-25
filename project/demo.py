

class Demo(object):
    def __init__(self):
        print("init.../")
        Demo.sultion()

    @staticmethod
    def sultion():
        print("static method")


if __name__ == '__main__':
    d = Demo()
