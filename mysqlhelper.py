import pymysql
db = pymysql.connect(host = 'localhost',
                     user = 'root',
                     password ='Xss040316',
                     database = 'test',
                     charset = 'utf8')
cursor = db.cursor() #游标
cursor.execute("SELECT VERSION()")
data = cursor.fetchone() #取出查询结果中的下一行（one row）
print("连接成功")
class MysqlHelper(object):
    conn_params = {
        'host': 'localhost',
        'port': 3306,
        'user': 'root',
        'password': 'Xss040316',
        'db': 'mysql',
        'charset': 'utf8'
    }   #与mysql建立连接

    def __init__(self, conn_params):    #初始化实例属性
        self.__host = conn_params['host']
        self.__port = conn_params['port']
        self.__db = conn_params['db']
        self.__user = conn_params['user']
        self.__password = conn_params['password']
        self.__charset = conn_params['charset'] #正在被创建的那一个实例

    def __connect(self): #建立数据库连接和打开游标
        self.__conn = connect(host=self.__host,
                              port=self.__port,
                              db=self.__db,
                              user=self.__user,
                              password=self.__password,
                              charset=self.__charset)
        self.__cursor = self.__conn.cursor() #关闭游标和关闭连接
    def __close(self):
        self.__cursor.close()
        self.__conn.close()

    def get_one(self, sql, params):  #获取一条数据
        result = None
        try:
            self.__connect()
            self.__cursor.execute(sql, params)
            result = self.__cursor.fetchone()
            self.__close()
        except Exception as e:
            print(e)
        return result

    def get_all(self, sql, params): #获取所有数据
        result1 = ()
        try:
            self.__connect()
            self.__cursor.execute(sql, params)
            result1 = self.__cursor.fetchall()
            self.__close()
        except Exception as e:
            print(e)
        return result1

    def insert(self, sql, params): #增加数据
        return self.__edit(sql, params)

    def update(self, sql, params):  #修改数据
        return self.__edit(sql, params)

    def delete(self, sql, params):  #删除数据
        return self.__edit(sql, params)

    def __edit(self, sql, params):  #增删改数据
        count = 0
        try:
            self.__connect()
            count = self.__cursor.execute(sql, params)
            self.__conn.commit()
            self.__close()
        except Exception as e:
            print(e)
        return count






