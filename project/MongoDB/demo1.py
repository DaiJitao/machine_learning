import pymongo

"""https://www.jianshu.com/p/08c384bef2e4"""

connect = pymongo.MongoClient("mongodb://localhost:27017/")
mydb = connect.list_database_names()
print(mydb)
runoob_db = connect.runoob