import pymysql


class MySQL():
    def __init__(self, host, user, pwd, db, tb, port=3306, charset="utf8"):
        self.host = 'localhost'
        self.user = user
        self.password = pwd
        self.db = db
        self.port = port
        self.tb = tb
        self.charset = charset
        self.connection = pymysql.connect(host=host, user=user, password=pwd, db=db, port=port, charset=charset)

    def update_data(self):
        with self.connection.cursor(cursor=pymysql.cursors.DictCursor) as cursor:
            sql = 'SELECT * FROM ' + self.tb + " where user_id=111 ORDER BY time_update DESC LIMIT 1;"
            print(sql)
            count = cursor.execute(sql)

            sql_result = cursor.fetchone()
            print(sql_result==None)


if __name__ == '__main__':
    mysql = MySQL(host='localhost', user='root', pwd='123', db='statistic_db', tb='douyin_detail_tb')
    mysql.update_data()