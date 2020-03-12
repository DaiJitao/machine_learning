import configparser

cf = configparser.ConfigParser()
cf.read("./config.ini")
data = cf.sections()
print(data)
host = cf.get(data[0], 'host')
print(data[0], 'host')
print(host)
print(cf.get(data[1], 'type'))
print(type(cf.get(data[1], "interval")))