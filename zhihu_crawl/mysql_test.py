import pymysql
from datetime import datetime

article = {
    'title': 'date123',
    'summary': 'week',
    'url': 'temperature',
    'url_code': 'weather12',
    'img_url': 'img_url',
    'author': 'author',
    'content': 'orgin_content',
    'create_user_id': 1,
    'update_user_id': 1
}

host = 'localhost'
user = 'root'
passwd = 'root'
db = 'aitprestprod'
charset = 'utf8mb4'
cursorclass=pymysql.cursors.DictCursor

def saveArticle2DB(article):
    # 将item里的数据拿出来
    title = article['title']
    summary = article['summary']
    url = article['url']
    url_code = article['url_code']
    img_url = article['img_url']
    author = article['author']
    content = article['content']
    create_user_id = article['create_user_id']
    update_user_id = article['update_user_id']

    # 和本地的scrapyDB数据库建立连接

    connection = pymysql.connect(
        host= host,  # 连接的是本地数据库
        user= user,  # 自己的mysql用户名
        passwd= passwd,  # 自己的密码
        db= db,  # 数据库的名字
        charset= charset,  # 默认的编码方式：
        cursorclass=cursorclass)

    try:
        with connection.cursor() as cursor:
            # duplication check
            if isDuplicatedUrlCode(url_code):
                print("Title:" + title + ", was already existed, continue...")
            else:
                # 创建更新值的sql语句
                dt = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

                sql = """
                    INSERT INTO article_referral(
                        origin_title,
                        origin_summary,
                        origin_url,
                        origin_url_code,
                        origin_img_url,
                        author,
                        orgin_content,
                        create_user_id,
                        create_date,
                        update_user_id,
                        update_date)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                    """
                # 执行sql语句
                # excute 的第二个参数可以将sql缺省语句补全，一般以元组的格式
                cursor.execute(
                    sql,
                    (title,
                     summary,
                     url,
                     url_code,
                     img_url,
                     author,
                     content,
                     create_user_id,
                     dt,
                     update_user_id,
                     dt))

        print("All data has been done....")
        # 提交本次插入的记录
        connection.commit()
    finally:
        # 关闭连接
        connection.close()


def isDuplicatedUrlCode(url_code):
    connection = pymysql.connect(
        host=host,  # 连接的是本地数据库
        user=user,  # 自己的mysql用户名
        passwd=passwd,  # 自己的密码
        db=db,  # 数据库的名字
        charset=charset,  # 默认的编码方式：
        cursorclass=cursorclass)
    try:
        with connection.cursor() as cursor:
            # duplication check
            sql = "select * from article_referral where origin_url_code='" + url_code + "'"
            count = cursor.execute(sql)
            return count > 0
    finally:
        # 关闭连接
        connection.close()


if __name__ == '__main__':
    saveArticle2DB(article)
