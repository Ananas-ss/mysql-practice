import pymysql
db = pymysql.connect(host = 'localhost',
                     user = 'root',
                     password ='Xss040316',
                     database = 'test',
                     charset = 'utf8')
cursor = db.cursor()
cursor.execute("SELECT VERSION()")
data = cursor.fetchone()
print("连接成功")
db.close