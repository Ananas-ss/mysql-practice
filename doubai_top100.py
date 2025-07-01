import requests
from mysql_helper import MysqlHelper
from lxml import etree
import pymysql
db = pymysql.connect(
    host="localhost",
    user="root",
    password="Xss040316",
    database="test",
    charset="utf8mb4"
)
cursor = db.cursor()
cursor.execute("DROP TABLE IF EXISTS douban_top100")
sql = """
CREATE TABLE douban_top100 (
    id        INT AUTO_INCREMENT PRIMARY KEY, 
    rank_no   INT         NOT NULL,
    title     VARCHAR(255) NOT NULL,
    date      SMALLINT,
    rating    DECIMAL(3,1),
    comCount     INT,
    genres    VARCHAR(255),
    country   VARCHAR(100),
    director  VARCHAR(255),
    UNIQUE KEY uk_rank (rank_no)
) CHARSET=utf8mb4;
"""

try:
    cursor.execute(sql)
    db.commit()
    print("创建 douban_top100 表成功！")
except Exception as e:
    db.rollback()
    print(f"创建表失败：{e}")

url = "https://movie.douban.com/top250?start=75&filter="
headers = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.3 Safari/605.1.15"
}
Top = 1
def getInfo(url):
    html = requests.get(url, headers=headers, timeout=30)
    print(html.status_code)
    root = etree.HTML(html.content)
    for InformationBlock in root.xpath('//div[@class="info"]'):
        title = InformationBlock.xpath('div[@class="hd"]/a/span[@class="title"]/text()')[0]
        info = InformationBlock.xpath('div[@class="bd"]/p[1]/text()')

        '''
                导演主演 info[0]
        '''
        directorAndStarring = str(info[0]).split("   ")
        director = directorAndStarring[0].replace(" ", "").replace("\n", "").replace("导演:", "")
        try:
            Starring = directorAndStarring[1].replace(" ", "").replace("\n", "").replace("主演:", "")
        except :
            Starring = "NULL"

        '''
        上映日期、制片国家、影片类型 info[1]
        '''
#上映日期
        date = info[1].replace(" ", "").replace("\n", "").split("/")[0]
#国家
        country = info[1].replace(" ", "").replace("\n", "").split("/")[1]
#影片类型
        geners = info[1].replace(" ", "").replace("\n", "").split("/")[2]
#评分
        rate = InformationBlock.xpath('div[@class="bd"]/div/span[2]/text()')[0]
#评论人数
        comCount = InformationBlock.xpath('div[@class="bd"]/div/span[4]/text()')[0].replace("人评价", "")
#赋值/重新绑定 全局变量
        global Top
        print(Top, title, director, Starring, rate, date, country, geners, comCount)
        print("---------------------------------------------------------")#分割线
        datas = (("{},{},{},{},{},{},{},{},{}").format(Top, title, director, Starring, rate, date, country, geners, comCount))
        with open("doubanMovie.csv", "a", newline="", encoding="utf_8_sig") as f:
            f.write(datas+"\n")
        Top += 1

# 翻页
def nextPage():
    for i in range(0, 100, 25):
        url = 'https://movie.douban.com/top250?start={}&filter='.format(i)
        getInfo(url)


if __name__ == '__main__':
    with open("doubanMovie.csv", "w", newline="", encoding="utf_8_sig") as f:
        f.write("Top,title,director,Starring,rate,date,country,geners,comCount"+"\n")
    nextPage()

db_helper = MysqlHelper(MysqlHelper.conn_params)

movies = [
    (1, '肖申克的救赎', 1994, 9.7, 2974289, '剧情/犯罪', '美国', '弗兰克·德拉邦特'),
    (2, '霸王别姬',     1993, 9.6, 1154794, '剧情/爱情', '中国大陆/香港', '陈凯歌'),
]
insert_sql = """
REPLACE INTO douban_top100
  (rank_no, title, date, rating, comCount, genres, country, director)
VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
"""

try:
    cursor.executemany(insert_sql, movies)
    db.commit()
    print("写入成功！")
except Exception as e:
    db.rollback()
    print(f"写入失败：{e}")
cursor.close()
db.close()
