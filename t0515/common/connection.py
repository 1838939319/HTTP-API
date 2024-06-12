from t0515.conf.operationConfig import Operation
from t0515.common.recodelog import logs
import pymysql

conf = Operation()
class ConnectMysql:
    def __init__(self):
        mysql_conf = {
            "host": conf.get_mysql_data("host"),
            "port": int(conf.get_mysql_data("port")),
            "username": conf.get_mysql_data("username"),
            "password": conf.get_mysql_data("password"),
            "database": conf.get_mysql_data("database")
        }
        try:
            self.conn = pymysql.connect(**mysql_conf,charset="utf8")
            #cursor=pymysql.cursors.DictCursor:将数据库表字段显示，以key:value形式显示
            self.cursor = self.conn.cursor(cursor=pymysql.cursors.DictCursor)
            logs.info("""
            数据库连接成功，
            host：{host}
            port:{port}
            db:{database}
            """.format(**mysql_conf))
        except Exception as e:
            logs.error(e)
    def colse(self):
        """查询数据"""
        if self.conn and self.cursor:
            self.cursor.close()
            self.conn.close()
    def query(self,sql):
        try:
            self.cursor.execute(sql)#执行sql
            self.conn.commit() #提交事务
            res = self.cursor.fetchall()#获取数据
            return res
        except Exception as e:
            logs.error(e)
        finally:
            self.colse()

    def insert(self,sql):
        pass

    def update(self,sql):
        pass

    def delete(self,sql):
        pass