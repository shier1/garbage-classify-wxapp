import pymysql

def get_db():
    db = pymysql.connect(
        host="10.0.224.15",
        port=3306,
        user="shier",
        password="ZhouYanPing187419",
        database="garbage_classify"
    )
    return db

def add_user_info(db:pymysql.connections.Connection, account:str, password:str):
    with db.cursor() as cursor:
        cursor.execute("insert into userLoginInfo values(%s, %s)", (account, password))
        db.commit()


def add_wx_login(db:pymysql.connections.Connection, openid:str):
    with db.cursor() as cursor:
        cursor.execute("select * from wxLoginInfo where openid=%s", (openid))
        if cursor.fetchone() is None:
            cursor.execute("insert into wxLoginInfo values (%s)", (openid))
            db.commit()
            

def query_exist_user_account(db:pymysql.connections.Connection, account:str):
    with db.cursor() as cursor:
        cursor.execute("select * from userLoginInfo where userAccount=%s", (account))
        exist_account = cursor.fetchone()
        return exist_account