import pymysql
from app.sql import add_wx_login

db = pymysql.connect(

    host="sh-cynosdbmysql-grp-0jsgrn5q.sql.tencentcdb.com",
    port=21632,
    user="shier",
    password="ZhouYanPing187419",
    database="garbage_classify"
)

print(type(db))

def query_exist_account(db, account):
    with db.cursor() as cursor:
        cursor.execute("")
        exist_account = cursor.fetchone()
        return exist_account

def test():
    add_wx_login(db=db, openid="12345")

if __name__ == "__main__":
    test()