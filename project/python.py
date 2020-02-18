class Test(object):
    a = 1

    def __del__(self):
        print("del ... ")


class Base():
    def __init__(self, name):
        self.name = name

    def get_name(self):
        return self.name


class B(Base):
    pass


class Animal(object):
    def __init__(self):
        pass

    def say(self):
        pass


class Dog(Animal):
    @staticmethod
    def say():
        print("wang ")


class Cat(Animal):
    def say(self):
        print("miao...")


class Tool():
    count = 0

    def __init__(self):
        Tool.count += 1

    @classmethod
    def show_count(cls):
        print("熟练", cls.count)


if __name__ == '__main__':
    from urllib.parse import urlparse, parse_qs

    url = "http://v6-default.ixigua.com/8908de3635850f48175bb683ad405d34/5e451891/video/tos/cn/tos-cn-ve-31/7cacfa9ccb584c11a4969d8fc9368a46/?a=2011&br=0&bt=412&cr=0&cs=0&dr=0&ds=1&er=&l=202002131632340100150431472158E248&lr=&qs=0&rc=ajNyampubHlpczMzNmkzM0ApOWdkODo7ZjwzN2QzZDM3O2dubG1gcV9jMS9fLS0tLi9zcy4xMGA0MF4xL142Yy9hYjI6Yw%3D%3D"

    parsed_tuple = urlparse(url)
    print(parsed_tuple)
    print(parsed_tuple.query)
    parse_qs_dict = parse_qs(parsed_tuple.query)
    print(parse_qs_dict)
    params = {key: parse_qs_dict[key][0] for key in parse_qs_dict}
    del params['l']
    print(params)
    try:
        start_index_p = url.index("?")
        start_index = url.index("&l=")
        end_index = url.index("&lr=")
        print(start_index, end_index)
        print(url[: start_index_p])
    except Exception as e:
        print(e)
