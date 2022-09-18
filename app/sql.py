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

def query_device_url_openid(db:pymysql.connections.Connection, openid:str):
    with db.cursor() as cursor:
        cursor.execute("select * from deviceInfo where openid=%s", (openid))
        res = cursor.fetchall()
        return res

def query_device_url_account(db:pymysql.connections.Connection, account:str):
    with db.cursor() as cursor:
        cursor.execute("select * from deviceInfo where userAccount=%s", (account))
        res = cursor.fetchall()
        return res

def add_devie_url(db:pymysql.connections.Connection, device_url:str, account:str, openid:str, device_name:str):
    with db.cursor() as cursor:
        cursor.execute("select * from deviceInfo where openid=%s", (device_url))
        res = cursor.fetchall()
        for res_userAccount, res_openid, _, _ in res:
            if res_userAccount == account and res_openid == openid:
                break
        else:
            cursor.execute("insert into deviceInfo values (%s,%s,%s,%s)" (account, openid, device_url, device_name))
            db.commit()

def delete_device_url(db:pymysql.connections.Connection, device_url:str, account:str, openid:str):
    with db.cursor() as cursor:
        cursor.execute("delete from deviceInfo where userAccount=%s and openid=%s and deviceUrl=%s" (account, openid, device_url))
        db.commit()


def query_forgetpd_question(db:pymysql.connections.Connection, account):
    with db.cursor() as cursor:
        cursor.execute("select * from forgetInfo where userAccount=%s", (account))
        res = cursor.fetchone()
        return res

def add_forgetpd_question(db:pymysql.connections.Connection, account, question1, question2, question3):
    with db.cursor() as cursor:
        cursor.execute("select * from forgetInfo where userAccount=%s", (account))
        res = cursor.fetchone()
        if res is None:
            cursor.execute("insert into forgetInfo values (%s,%s,%s,%s)" (question1, question2, question3, account))
            db.commit()
        else:
            return

def alter_user_paddword(db:pymysql.connections.Connection, account, password):
    with db.cursor() as cursor:
        cursor.execute("update userLoginInfo set userPassWd=%s where userAccount=%s" (password, account))
        db.commit()