# -*- coding: utf-8 -*-
"""
    数据库连接类
    @author: h
"""

import pymssql
import pandas as pd


class SqlServerConnect:

    def __init__(self, ip="192.168.12.111",user="pengs", password="pengs0410", database="cd_10_sec"):
        self.ip = ip
        self.user = user
        self.password = password
        self.database = database
        self._conn = self.getConnect()
        self._cur = self._conn.cursor()

    # 连接数据库
    def getConnect(self):
        conn = pymssql.connect(server=self.ip, user=self.user,
                               password=self.password, database=self.database)
        return conn

    # 执行查询
    def exeQuery(self,sql,columns):
        res = ""
        try:
            self._cur.execute(sql)
            res = self._cur.fetchall()
            resDf = pd.DataFrame(list(res))
            resDf.columns = columns
        except Exception as e:
            return None
        else:
            return resDf

    # 执行非查询类语句
    def exeNonQuery(self, sql, multi=False):
        try:
            if not multi:
                self._cur.execute(sql)
            else:
                for result in self._cur.execute(sql, multi=True):
                    pass
            self._conn.commit()
            return True
        except Exception as e:
            # print("执行sql异常:"+sql)
            with open('error_sql.txt', 'w') as f:
                f.write(sql)
            raise Exception("执行sql异常:"+str(e))

    # 获取连接信息
    def getConnectInfo(self):
        print("连接信息")
        print("服务器：%s ,用户名：%s , 数据库：%s " %(self.host,self.user,self.database))

    def close(self):
        try:
            self._cur.close()
            self._conn.close()
        except:
            print("关闭异常：%s,%s" %(type(self._cur),type(self._conn)))
            raise("关闭异常：%s,%s" %(type(self._cur),type(self._conn)))


if __name__ == "__main__":

    ssc = SqlServerConnect(database="CD_10_SEC")
    begin_date = "2018-01-01"
    end_date = "2020-03-19"
    sql = "select sec_cd,pub_dt,F0010,F0020,F0030,F0040,F0050,F0060,F0070 from dbo.QOT_D_BCK " \
          "where pub_dt>='%s'and pub_dt<= '%s' and is_vld = 1 and var_cl = 'a' " \
          "and mkt_cl in ('s','z') and sec_cd='601777' and f0060 > 0 " \
          "order by pub_dt " % (begin_date, end_date)
    df = ssc.exeQuery(sql, ["stock_code", "date", "preclose", "open", "high", "low", "close",
                            "volume", "turnover"])
