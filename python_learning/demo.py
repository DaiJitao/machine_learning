

class A():

    def fly(self):
        print('A fly')

class B():

    def fly(self):
        print("B fly")

class C(A,B):
    def __init__(self):
        print(__class__)
        super().__init__()


    # def fly(self):
    #     super().fly()

if __name__ == '__main__':
    c = C()

    print(C.mro() )