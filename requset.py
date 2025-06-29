from mysql_helper import MysqlHelper
import requests
from bs4 import BeautifulSoup

import pymysql
db = pymysql.connect(host = 'localhost',
                     user = 'root',
                     password ='Xss040316',
                     database = 'test',
                     charset = 'utf8')
cursor = db.cursor() #游标
cursor.execute("DROP TABLE IF EXISTS 百度热搜榜top10")
sql = """
    create table 百度热搜榜top10(            
    排名  int          null,
    内容  varchar(255) null
)
"""
try:
    cursor.execute(sql)
    print("创建数据库成功")
except Exception as e:
    print("创建数据库失败：case%s" % e)

url = "https://top.baidu.com/board?tab=realtime"
headers = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.3 Safari/605.1.15"
}
response = requests.get(url,  headers = headers)
html = response.text
soup = BeautifulSoup(html, features = "html.parser")
kw = soup.select("div .c-single-text-ellipsis")
count = soup.select("div .hot-index_1Bl1a")

context = []
for i in range(min(len(kw),10)):
    k = kw[i].text.strip()
    v = count[i].text.strip()
    context.append((i + 1, k))
for j in context:
    print(j)
db_helper = MysqlHelper(MysqlHelper.conn_params)
insert_sql = """
    INSERT INTO 百度热搜榜top10 (排名, 内容)
    VALUES (%s, %s)
"""
try:
    for item in context:
        cursor.execute(insert_sql, item)
    db.commit()
    print("写入成功！")
except Exception as e:
    db.rollback()
    print(f"写入失败：{e}")
cursor.close()
db.close()







