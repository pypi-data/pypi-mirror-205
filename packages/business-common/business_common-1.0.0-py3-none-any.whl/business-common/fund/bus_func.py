import math
import logging
import numpy as np
import pandas as pd
from datetime import datetime
from fund_sql import FundDataAccess
from public_func import CommonTools
from SqlServer_Connect import SqlServerConnect

class FundDataHandler:
    def __init__(self):
        self.end = datetime.today().strftime('%Y%m%d')
        self.db_config = CommonTools.read_conf("db")

    def fetch_calendar(self, start="19900101", end=None):
        """
        获取中日交易日历，标准化日期返回list列表
        :param start: 开始日期（默认为19900101）
        :param end: 结束日期（默认为当前日期）
        :return: list列表
        """
        if end is None:
            end = self.end

        res = FundDataAccess.calendar_sql(start, end)['pub_dt'].to_list()

        return res


    def check_trade_day(self, date):
        """
        检查是否为交易日，返回bool值
        :param date: 日期
        :return: bool值（True为交易日，False为非交易日）
        """
        try:
            dt_date = pd.to_datetime(date, format='%Y%m%d')
        except Exception as e:
            print(e)
        list = self.fetch_calendar()

        if dt_date not in list:
            return False

        return True


    def fetch_bm_returns(self, date, start="19900101", end=None):
        """
        确认市场基准：股票大盘、利率债、信用，获取市场基准的收益率，返回DataFrame对象
        :param date: 日期
        :param start: 开始日期（默认为1990-01-01）
        :param end: 结束日期（默认为今天）
        :return: DataFrame对象
        """

        if end is None:
            end = self.end

        # 因为很多基金周末也公布净值，所以要调整交易日历，以使得和正常的交易日历一样
        calendar = pd.to_datetime(self.fetch_calendar(end=date))
        # 确定市场基准, 股票大盘：中证全指(000985)，利率债：中证国债(H11006)，信用：中证企业债(H11008)
        bm_index = FundDataAccess.bm_sql(sid=('000985', 'H11006', 'H11008'), start=start, end=end) \
            .set_index(['date', 'idx_cd'])['closeprice'].unstack().sort_index()
        bm_index.columns.name = None

        bm_returns_total = bm_index.rename(columns={'000985': 'stock', 'h11006': 'treasury', 'h11008': 'credit'}) \
            .reindex(calendar).pct_change().fillna(0)

        bm_returns_total = bm_returns_total.reset_index().rename(columns={'index': 'date'})

        return bm_returns_total

    def historical_trading_day(self, date):
        """
        获取历史交易日信息
        :param date: 日期（格式为Y-M-D）
        :return: 返回历史交易日信息
        """

        start_date = self.check_trade_day(date)

        if start_date:

            hist_dt = FundDataAccess.fetch_com_dt_hist(date)

            pef_horizions = {
                '1w': hist_dt.loc['B1W'].strftime('%Y%m%d'),
                '1m': hist_dt.loc['B1M'].strftime('%Y%m%d'),
                '3m': hist_dt.loc['B3M'].strftime('%Y%m%d'),
                '6m': hist_dt.loc['B6M'].strftime('%Y%m%d'),
                '1y': hist_dt.loc['B1Y'].strftime('%Y%m%d'),
                '3y': hist_dt.loc['B3Y'].strftime('%Y%m%d'),
                '5y': hist_dt.loc['B5Y'].strftime('%Y%m%d'),
                'ytd': hist_dt.loc['END_LAST_YR'].strftime('%Y%m%d')

            }
            return pef_horizions

        else:
            logging.error("Please enter the correct transaction date")


    def fetch_funds_list(self, fund_type, is_run_history=False):
        """
        获取所有基金数据，返回list列表
        :param fund_type: 传参选择：mny_sids/sids，mny_sids：所有非货币基金数据，sids：所有货币基金数据
        :param is_run_history: 是否取未退市的基金（默认为False）
        :return: 返回list列表
        """

        df = FundDataAccess.funs_sql(is_run_history)
        try:
            if fund_type == "mny_sids":
                sid_df = df[(~df.F1010.isin([6])) & (df.is_vld.isin([True]))]['sec_id'].squeeze().tolist()
            elif fund_type == "sids":
                sid_df = df[(df.F1010.isin([6])) & (df.is_vld.isin([True]))]['sec_id'].squeeze().tolist()

            return sid_df
        except:
            logging.warn("Please enter 'mny_sids' or 'sids' parameter")


    def get_nav_total(self, date, is_fetch_history=False, is_filter_null=False, sec_id_list=None):
        """
        获取所有基金的净值，基于数据源所有基金拆分为货币基金和非货币基金
        :param date: 日期
        :param is_fetch_history: 是否取未退市的基金
        :param is_filter_null: 是否过滤date当日未披露净值的基金 日常更新时指定为TRUE
        :param sec_id_list: 指定基金列表
        :return: 所有基金的净值，只包含有效的净值数据(对于nav去掉空值和0，对于ret去掉空值)
        """

        # 所有基金列表：非货币基金 + 货币基金
        universe = self.fetch_funds_list("mny_sids", is_fetch_history)
        universe_mny = self.fetch_funds_list("sids", is_fetch_history)
        # 得到非货币基金的净值
        nav = FundDataAccess.fetch_nav(end=date, sec_id_list=sec_id_list)

        # 得到货币基金的ret（日收益率）
        ret_mny = FundDataAccess.fetch_ret_mny(end=date, sec_id_list=sec_id_list)

        if is_filter_null:
            # 得到当日所有披露nav或ret的基金
            publish_sid_list = FundDataAccess.fetch_all_publish_sid(date)
            nav = nav[nav.sec_id.isin(publish_sid_list)]
            ret_mny = ret_mny[ret_mny.sec_id.isin(publish_sid_list)]
        nav_nom = nav[nav.sec_id.isin(universe)]

        nav_nom = nav_nom.drop_duplicates(subset=['date', 'sec_id'], keep='first')

        ret_mny = ret_mny[ret_mny.sec_id.isin(universe_mny)]

        # 货币基金中存在部分基金部分数据在净值表 部分数据在ret（万份收益）表 所以将其都转换为ret 统一起来
        nav_mny_etr = nav[nav.sec_id.isin(universe_mny)]

        if not nav_mny_etr.empty:
            nav_mny_etr = nav_mny_etr.drop_duplicates(subset=['date', 'sec_id'], keep='first')

            def get_pct_change(xdf):
                xdf = xdf.sort_values(by='date')

                # 数据库中存在个别货币基金在nav表中只有一条记录
                xdf['ret'] = xdf['nav'].pct_change().fillna(0)

                return xdf

            ret_mny_etr = nav_mny_etr.groupby('sec_id', group_keys=True).apply(lambda x: get_pct_change(x)).drop(
                labels='nav', axis=1)

            ret_mny = pd.concat([ret_mny, ret_mny_etr], ignore_index=True)

        if not ret_mny.empty:
            ret_mny = ret_mny.drop_duplicates(subset=['date', 'sec_id'], keep='first')

            # 将所有货币基金的ret转换为nav 因为非交易日也存在ret 需要将非交易日的ret挪到交易日上去
            def get_cumprod(xdf):
                xdf = xdf.sort_values(by='date')
                xdf['nav'] = (xdf['ret'] + 1).cumprod()
                return xdf

            nav_mny = ret_mny.groupby('sec_id', group_keys=True).apply(lambda x: get_cumprod(x)).drop(labels='ret', axis=1)

        else:
            nav_mny = pd.DataFrame()
        nav_total = pd.concat([nav_nom, nav_mny], ignore_index=True)
        return nav_total[['date', 'sec_id', 'nav']]


    def fill_na_for_nav_total_in_trade_day(self, date, nav_total_df):
        """
        nav_total_df 中间的交易日 以空值填充
        :param date: 日期
        :param nav_total_df: 净值df，包含交易日的净值和非交易日的净值，
        并非所有的交易日都有净值，待补全 ,df中date格式为字符串:%Y-%m-%d
        :return: 净值df，包含交易日的净值和非交易日的净值，基金披露净值以来所有交易日均有净值(包括空值)
        """

        trade_day_list = self.fetch_calendar(end=date)

        def fill_na_for_trade_day(xdf):
            xdf = xdf.sort_values('date')
            the_first_date = xdf.iloc[0]['date']
            the_last_date = xdf.iloc[-1]['date']
            sec_id = xdf.iloc[0]['new_sec_id']
            the_trade_day_list = [trade_day for trade_day in trade_day_list if the_first_date <= trade_day <= the_last_date]
            xdf = xdf.set_index('date').reindex(the_trade_day_list).reset_index()
            xdf['new_sec_id'] = sec_id
            return xdf

        # 以sec_id 分组 不要在分组中直接使用这个字段 需要备份一个
        nav_total_df['new_sec_id'] = nav_total_df['sec_id']
        # 得到补全交易日的净值数据 去掉非交易日的净值数据
        # nav_total_in_trade_day_df = nav_total_df.groupby('sec_id').apply(lambda x: fill_na_for_trade_day(x))\
        #     .reset_index(drop=True)
        nav_total_in_trade_day_df = nav_total_df.groupby('sec_id').apply(lambda x: fill_na_for_trade_day(x),
                                                                         meta=nav_total_df) \
            .reset_index(drop=True)
        nav_total_in_trade_day_df = nav_total_in_trade_day_df[['date', 'new_sec_id', 'nav']].rename(
            columns={'new_sec_id': 'sec_id'})
        # 把非交易日的净值数据补充回去
        nav_total_all = pd.concat([nav_total_df, nav_total_in_trade_day_df], ignore_index=True) \
            .drop_duplicates(subset=['sec_id', 'date'], keep='first')

        return nav_total_all


    def get_ret_total(self, date, nav_total_df):
        """
        得到基金的ret
        :param date: 日期
        :param nav_total_df: 净值df，包含交易日的净值和非交易日的净值，
        基金披露净值以来所有交易日均有净值(包括空值),df中date格式为字符串:%Y-%m-%d
        :return: ret_df ,只有交易日的ret,披露净值以来所有交易日均有ret(包括0)
        """

        # 先前向填充 再过滤非交易日
        def ffill_na(xdf):
            xdf = xdf.sort_values('date')
            xdf['nav'] = xdf['nav'].fillna(method='ffill')
            return xdf

        nav_total_df = nav_total_df.groupby('sec_id').apply(lambda x: ffill_na(x),
                                                            meta={"date": "datetime64[ns]", "sec_id": object, "nav": float,
                                                                  "new_sec_id": object}).reset_index(drop=True)
        estab_dt_df = FundDataAccess.fetch_estab_dt()  # 取成立日期 保证大于成立日期

        nav_total_df = pd.merge(nav_total_df, estab_dt_df, on=['sec_id'], how='inner')
        nav_total_df = nav_total_df[nav_total_df.date >= nav_total_df.estab_dt]
        trade_day_list = self.fetch_calendar(end=date)
        nav_total_df = nav_total_df[nav_total_df.date.isin(trade_day_list)]

        def get_ret(xdf):
            xdf = xdf.sort_values('date')
            # pct_change会将空值填为0(除了第一行)
            xdf['ret'] = xdf['nav'].pct_change().fillna(0)
            return xdf

        ret_total_df = nav_total_df.groupby('sec_id').apply(lambda x: get_ret(x),
                                                            meta={"date": "datetime64[ns]", "sec_id": object, "nav": float,
                                                                  "new_sec_id": object, 'estab_dt': "datetime64[ns]",
                                                                  'ret': float}).reset_index(drop=True)

        return ret_total_df[['date', 'sec_id', 'nav', 'ret']]


    def into_db(self, date, df, table_name):
        """
        用于update or insert 基金评价相关的五张表 主键 sec_id pub_dt
        含字符串的列 ret_start（datetime会自动转换）
        其他为数值型的列 最大保留6位小数 （int 4位小数 会自动转换）
        :param date: 需要更新的日期(主键的pub_dt)
        :param df: 入库DataFrame
        :param table_name: 入库表名
        :return:
        """
        df = df.replace([np.inf, -np.inf], np.nan)
        # 经过文件的拼接和转换之后 inf可能会转换成字符串
        df = df.replace('-Infinity', np.nan)
        df = df.replace('Infinity', np.nan)
        # 出现过一次替换不成功的情况(原因未知)
        df = df.replace('-Infinity', None)
        df = df.replace('Infinity', None)
        ssc = SqlServerConnect(ip=self.db_config['host'], user=self.db_config['user'], password=self.db_config['password'],
                               database='CD_10_IND')
        sql = """
        select sec_id,pub_dt from %s with(nolock) where pub_dt = '%s' 
        """ % (table_name, date)
        exist_df = ssc.exeQuery(sql, ['sec_id', 'pub_dt'])
        if exist_df is not None:
            exist_df['pub_dt'] = exist_df['pub_dt'].apply(lambda x: str(x)[:10])
            update_df = pd.merge(df, exist_df, on=['sec_id', 'pub_dt'], how='inner')
            update_sql = ""
            columns = update_df.columns.to_list()
            count = 0
            for index, row in update_df.iterrows():
                count += 1
                # print(count)
                tmp_update_sql = "update %s set updt_tm = getdate(),is_vld=1," % table_name
                for column_name in columns:
                    if column_name != 'sec_id' and column_name != 'pub_dt':
                        if column_name == 'ret_start':
                            if row[column_name] is not None:
                                tmp_update_sql += "%s='%s'," % (column_name, row[column_name])
                        else:
                            if row[column_name] is not None:
                                row[column_name] = float(row[column_name])
                                if not math.isnan(row[column_name]):
                                    tmp_update_sql += "%s=%.6f," % (column_name, row[column_name])
                tmp_update_sql = tmp_update_sql[:-1] + " where sec_id = '%s' and pub_dt = '%s';" % (
                row['sec_id'], row['pub_dt'])
                update_sql += tmp_update_sql
                if count % 1000 == 0:
                    ssc.exeNonQuery(update_sql)
                    update_sql = ""
                    logging.info("update sql执行成功")
            if count % 1000 != 0:
                ssc.exeNonQuery(update_sql)
                logging.info("不足1000的update sql执行成功")
            insert_df = df.append(update_df).reset_index(drop=True).drop_duplicates(subset=['sec_id', 'pub_dt'], keep=False)
        else:
            insert_df = df
        if not insert_df.empty:
            columns = insert_df.columns.to_list()
            insert_sql = "insert into %s (%s) values " % (table_name, ','.join(columns))
            count = 0
            for index, row in insert_df.iterrows():
                count = count + 1
                # print(count)
                tmp_insert_sql = "("
                for column_name in columns:
                    if column_name != 'sec_id' and column_name != 'pub_dt' and column_name != 'ret_start':
                        if row[column_name] is not None:
                            row[column_name] = float(row[column_name])
                            if not math.isnan(row[column_name]):
                                tmp_insert_sql += "%.6f," % row[column_name]
                            else:
                                tmp_insert_sql += "null,"
                        else:
                            tmp_insert_sql += "null,"
                    else:
                        if row[column_name] is not None:
                            tmp_insert_sql += "'%s'," % row[column_name]
                        else:
                            tmp_insert_sql += "null,"
                insert_sql += tmp_insert_sql[:-1] + "),"
                if count % 1000 == 0:
                    insert_sql = insert_sql[:-1] + ';'
                    ssc.exeNonQuery(insert_sql)
                    insert_sql = "insert into %s (%s) values " % (table_name, ','.join(columns))
                    logging.info('insert sql执行成功')
            if count % 1000 != 0:
                insert_sql = insert_sql[:-1] + ';'
                ssc.exeNonQuery(insert_sql)
                logging.info('不足1000的insert sql执行成功')
        else:
            logging.info('没有数据需要插入')
        ssc.close()

if __name__ == "__main__":
    fd = FundDataHandler()
    print(fd.fetch_calendar('2019-01-01', '2019-01-31'))
    print(fd.check_trade_day('20190101'))
    print(fd.historical_trading_day('20230105'))
    print(fd.get_nav_total('20230101', '20230131', '000001'))