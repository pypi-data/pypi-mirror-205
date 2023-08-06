import yaml
import pyhdfs
import pandas as pd
from sqlalchemy import create_engine

class CommonTools:
    def __init__(self):
        pass

    def read_conf(self, path, name):
        """
        读取配置文件，返回配置信息
        :param path: yml配置文件路径
        :param name: 配置文件中的key：db, tables, hdfs
        :return: 配置信息
        """

        with open(path, encoding = "UTF-8") as f:
            conf = yaml.load(f, Loader=yaml.SafeLoader)

        return conf[name]

    def spark_mssql(self, spark):
        """
        SparkSQL连接配置，返回DataFrame
        :param spark: SparkSession对象
        :return: DataFrame
        """

        db_config = self.read_conf("db")
        df = spark.read.format("jdbc") \
            .option("url", "jdbc:sqlserver://%s".format(db_config['host'])) \
            .option("database", db_config['database']) \
            .option("dbtable", "DBO.QOT_D_COM_DT_HIST") \
            .option("user", db_config['user']) \
            .option("password", db_config['password']) \
            .option("driver", "com.microsoft.sqlserver.jdbc.SQLServerDriver") \
            .load()

        return df

    def py_hdfs(self, host, user_name, port = 50070):
        """
        hdfs连接 配置，返回HdfsClient对象
        :param host: Hadoop平台的ip地址
        :param user_name: 连接的Hadoop平台用户名
        :param port: HDFS端口号（默认为50070）
        :return: HdfsClient对象
        """

        # host = '192.168.137.100'
        client = pyhdfs.HdfsClient(hosts = ["%s:%d" % (host, port)],
                                   timeout = 3,  # 超时时间，单位秒
                                   max_tries = 3,  # 节点重连秒数
                                   retry_delay = 5,  # 在尝试连接一个Namenode节点失败后，尝试连接下一个Namenode的时间间隔，默认5sec
                                   user_name = user_name,  # 连接的Hadoop平台的用户名
                                   randomize_hosts = True,  # 随机选择host进行连接，默认为True
                                   )
        return client


    def read_sql(self, sql):
        """
        SQLServer连接引擎，传入SQL语句，返回DataFrame
        :param sql: SQL语句
        :return: DataFrame对象
        """
        db_config = self.read_conf("db")
        engine = create_engine('mssql+pymssql://{user}:{password}@{host}'.format(**db_config))
        df = pd.read_sql(sql, con = engine)

        return df

if __name__ == '__main__':
    pb = CommonTools()
    db_config = pb.rd_conf("db")
    print(db_config)