from datetime import datetime
from public_func import CommonTools

class FundDataAccess:
    def __init__(self):
        self.pb = CommonTools()
        self.end = datetime.today().strftime('%Y%m%d')

    def calendar_sql(self, start, end):
        """
        查询中国交易日历，返回交易日历DataFrame对象
        :param start: 开始时间
        :param end: 结束时间
        :return: DataFrame对象
        """

        query = ("select distinct pub_dt from CD_10_IND.dbo.QOT_D_COM_DT_HIST with(nolock) where pub_dt between '{start}' and '{end}' and  is_vld = 1 order by pub_dt".format(start=start, end=end))
        df = self.pb.read_sql(query)

        return df

    def fetch_estab_dt(self):
        """
        查询所有基金成立日期，返回基金成立日期DataFrame对象
        :return: DataFrame对象
        """

        query = "select sec_id, estab_dt from cd_10_sec.dbo.fnd_d_fact with(nolock) where is_vld = 1 "
        res = self.pb.read_sql(query)
        return res

    def bm_sql(self, sid, start, end):
        """
        查询sid基准，输出交易日、sid、收盘价，返回DataFrame对象
        :param sid: 基准代码
        :param start: 开始时间
        :param end: 结束时间
        :return: DataFrame对象
        """

        query = ("select distinct pub_dt as date, lower(idx_cd) as idx_cd, F0050 as closeprice from CD_10_SEC.DBO.QOT_D_IDX with(nolock) "
                 "where idx_cd in {sid} and pub_dt between '{start}' and '{end}' and is_vld=1 "
                 .format(sid=sid, start=start, end=end))
        df = self.pb.read_sql(query)

        return df

    def fetch_com_dt_hist(self, date):
        """
        获取公司自己定义的horizon
        :param date: 日期
        :return: Series对象
        """

        query = "select * from CD_10_IND.DBO.QOT_D_COM_DT_HIST with(nolock) where pub_dt='%s' and is_vld =1 " % date
        res = self.pb.read_sql(query).squeeze()

        return res

    def fetch_com_dt_hist_df(self, start, end):
        """
        获取公司自己定义的horizon，返回DataFrame
        :param end: 结束日期
        :return: DataFrame对象
        """

        query = """
        select pub_dt as date,b1w,b1m,b3m,b6m,b1y,b3y,b5y,end_last_yr from CD_10_IND.DBO.QOT_D_COM_DT_HIST with(nolock)
        where pub_dt>='%s' 
        and pub_dt <= '%s' and is_vld = 1
        """ % (start, end)

        res = self.pb.read_sql(query)

        return res

    def fetch_fund_performance_ret(self, date, ret_table_name):
        """
        获取在交易日date所有基金的收益指标数据，返回DataFrame对象
        :param date: 日期
        :param ret_table_name: 收益指标表名
        :return: DataFrame对象
        """

        query = ("select a.sec_id, b.f1020 as fnd_type,cagr_1m,cagr_3m,cagr_6m,cagr_1y,cagr_3y,cagr_5y "
                 "from %s a with(nolock) "
                 "inner join CD_10_SEC.DBO.FND_D_TAG b with(nolock) on a.sec_id=b.sec_id and b.is_vld =1 "
                 "where a.pub_dt='%s' and a.is_vld = 1 " % (ret_table_name, date))
        res = self.pb.read_sql(query)

        return res

    def fetch_fund_performance_vol(self, date, vol_table_name):
        """
        获取在交易日date所有基金的收益指标数据，返回DataFrame对象
        :param date: 日期
        :param vol_table_name: 波动率指标表名
        :return: DataFrame对象
        """

        query = ("select a.sec_id, b.f1020 as fnd_type,vol_1m,vol_3m,vol_6m,vol_1y,vol_3y,vol_5y, "
                 "md_1m,md_3m,md_6m,md_1y,md_3y,md_5y, "
                 "dvol_1m,dvol_3m,dvol_6m,dvol_1y,dvol_3y,dvol_5y, "
                 "var_1m,var_3m,var_6m,var_1y,var_3y,var_5y "
                 "from %s a with(nolock) "
                 "inner join CD_10_SEC.DBO.FND_D_TAG b with(nolock) "
                 "on a.sec_id=b.sec_id and b.is_vld = 1 where a.pub_dt='%s' and a.is_vld =1 " % (vol_table_name, date))

        res = self.pb.read_sql(query)

        return res

    def fetch_fund_performance_comp(self, date,comp_table_name):
        """
        获取在交易日date所有基金的综合业绩指标数据，返回DataFrame对象
        :param comp_table_name: 综合业绩指标表名
        :return: DataFrame对象
        """

        query = ("select a.sec_id, b.f1020 as fnd_type,sharpe_1m,sharpe_3m,sharpe_6m,sharpe_1y,sharpe_3y,sharpe_5y, "
                 "sortino_1m,sortino_3m,sortino_6m,sortino_1y,sortino_3y,sortino_5y, "
                 "calmar_1m,calmar_3m,calmar_6m,calmar_1y,calmar_3y,calmar_5y, "
                 "treynor_1m,treynor_3m,treynor_6m,treynor_1y,treynor_3y,treynor_5y, "
                 "omega_1m,omega_3m,omega_6m,omega_1y,omega_3y,omega_5y, "
                 "tail_1m,tail_3m,tail_6m,tail_1y,tail_3y,tail_5y "
                 "from %s a with(nolock) "
                 "inner join CD_10_SEC.DBO.FND_D_TAG b with(nolock) "
                 "on a.sec_id=b.sec_id and b.is_vld = 1 where a.pub_dt='%s' and a.is_vld =1 " % (comp_table_name, date))

        res = self.pb.read_sql(query)

        return res

    def fetch_fund_performance_other(self, date,other_table_name):
        """
        获取在交易日date所有基金的其他指标数据，返回DataFrame对象
        :param other_table_name: 其他指标表名
        :return: DataFrame对象
        """

        query = (
                    "select a.sec_id, b.f1020 as fnd_type,stability_1m,stability_3m,stability_6m,stability_1y,stability_3y,stability_5y, "
                    "picking_1m,picking_3m,picking_6m,picking_1y,picking_3y,picking_5y,timing_1m,timing_3m, "
                    "timing_6m,timing_1y,timing_3y,timing_5y,te_1m,te_3m,te_6m,te_1y,te_3y,te_5y "
                    "from %s a with(nolock) inner join CD_10_SEC.DBO.FND_D_TAG b with(nolock) "
                    "on a.sec_id=b.sec_id and b.is_vld =1 where a.pub_dt='%s' and a.is_vld =1 " % (other_table_name,date))

        res = self.pb.read_sql(query)

        return res

    def fetch_fmgr_sco(self, date):
        """
        获取某基金在某日的不同期限的基金经理得分
        :param date: 日期
        :return: DataFrame对象
        """

        query = (";with tM as (SELECT distinct(m.pes_id) as pes_id, m.sec_id, t.f1020 FROM [CD_10_SEC].[dbo].[FND_D_FMGR] m with(nolock) "
                 "inner join [CD_10_SEC].[dbo].[FND_D_TAG] t with(nolock) on m.sec_id=t.sec_id and t.is_vld = 1 "
                 "WHERE m.f0140=1 and m.is_vld = 1 and "
                 "isnull(m.f0020,getdate())>'%s' and m.f0010<='%s') "
                 "SELECT b.sec_id, a.tag as fnd_type, isnull(avg(a.tot_1y),0.0) as fmgr_1m, isnull(avg(a.tot_1y),0.0) as fmgr_3m, "
                 "isnull(avg(a.tot_1y),0.0) as fmgr_6m, isnull(avg(a.tot_1y),0.0) as fmgr_1y, isnull(avg(a.tot_3y),0.0) as fmgr_3y, "
                 "isnull(avg(a.tot_5y),0.0) as fmgr_5y FROM [CD_10_IND].[dbo].[IND_S_FMGR_IND] a with(nolock) inner join tM b with(nolock) "
                 "on a.pes_id=b.pes_id and a.tag=b.f1020 where a.pub_dt='%s' and a.is_vld = 1 group by a.pub_dt, b.sec_id, a.tag" % (date,date,date))

        res = self.pb.read_sql(query)

        return res


    def funs_sql(self, is_run_history = False):
        """
        获取所有基金的基本信息，根据is_run_history判断是否是历史数据，返回DataFrame对象
        :param is_run_history: 是否是历史数据（默认为False）
        :return: DataFrame对象
        """

        if not is_run_history:
            query = """
            select distinct(f.sec_id), t.F1010, f.is_vld from CD_10_SEC.DBO.FND_D_FACT F with(nolock) INNER JOIN 
             CD_10_SEC.DBO.FND_D_TAG T with(nolock) on f.sec_id=t.sec_id and t.is_vld = 1 where (f.DEL_DT is null 
             or (f.DEL_DT is not null and f.DEL_DT > dateadd(day, -1, getdate()))) 
            """
        else:
            """历史数据删去del_dt is null"""
            query = """
            select distinct(f.sec_id),t.F1010, f.is_vld from CD_10_SEC.DBO.FND_D_FACT F with(nolock) INNER JOIN
            CD_10_SEC.DBO.FND_D_TAG T with(nolock) on f.sec_id=t.sec_id and t.is_vld =1 where
            not t.F1010=6 and f.is_vld = 1
            """

        df = self.pb.read_sql(query)

        return df

    def fetch_fund_nav_up_time_in_given_time_period(self, begin_date, end_date):
        """
        获取时间段内更新过净值的基金且常更新程序没有覆盖到基金(日常更新第二天23点更新前一天)，
        基金净值过了一个月后才更新不予考虑(节约计算成本)
        :param begin_date: 开始日期
        :param end_date: 结束日期
        :return: DataFrame对象
        """

        sql = """
        select distinct sec_id,f0010 as date from CD_10_SEC.DBO.FND_D_NTVAL with(nolock) where
        not F0060 = 0 and F0060 is not null and datediff(hour,f0010,UPDT_TM) >= 40
        and datediff(day,f0010,UPDT_TM) <= 30 and f0010 < '%s'
        and UPDT_TM >= '%s' and UPDT_TM <= '%s' and is_vld = 1
        union
        SELECT distinct sec_id,f0010 as date from [CD_10_SEC].[dbo].[FND_D_MKT_YIELD] with(nolock) WHERE is_vld = 1 
        and f0020 is not null and datediff(hour,f0010,UPDT_TM) >= 40
        and datediff(day,f0010,UPDT_TM) <= 30 and f0010 < '%s'
        and UPDT_TM >= '%s' and UPDT_TM <= '%s'
        """ % (begin_date, begin_date, end_date, begin_date, begin_date, end_date)

        res = self.pb.read_sql(sql)

        return res


    def fetch_bench_ret_up_time_in_given_time_period(self, begin_date, end_date):
        """
        更新时间在给定时间范围，主程序覆盖不到的更新
        :param begin_date: 开始日期
        :param end_date: 结束日期
        :return: DataFrame对象
        """

        sql = """
        select distinct pub_dt as date from CD_10_SEC.DBO.QOT_D_IDX with(nolock)
        where idx_cd in ('H11008','H11006','000985') and is_vld=1 and F0050 is not NULL 
        and datediff(hour,pub_dt,UPDT_TM) >=40 and datediff(day,pub_dt,UPDT_TM) <= 30
        and pub_dt < '%s' 
        and UPDT_TM >= '%s' and UPDT_TM <= '%s'
        union
        select distinct pub_dt as date from CD_10_IND.dbo.IND_S_FND_BENCH with(nolock) where stat_prd = 30 
        and is_vld = 1 and chg_ratio is not null 
        and datediff(hour,pub_dt,UPDT_TM) >=40 and datediff(day,pub_dt,UPDT_TM) <= 30
        and pub_dt < '%s'  
        and UPDT_TM >= '%s' and UPDT_TM <= '%s'
        """ % (begin_date, begin_date, end_date, begin_date, begin_date, end_date)

        res = self.pb.read_sql(sql)

        return res


    def fetch_all_publish_sid(self, date, is_run_history = False):
        """
        获取所有当日披露净值的基金或者所有未退市的基金，根据is_run_history判断是否是历史数据，返回DataFrame对象
        :param is_run_history: 是否是历史数据（默认为False）
        :return: DataFrame对象
        """

        if ~is_run_history:
            """得到所有当日披露净值的基金"""
            query = """
            select distinct sec_id from CD_10_SEC.DBO.FND_D_NTVAL with(nolock) where 
            not F0060 = 0 and F0060 is not null and f0010 = '%s' and is_vld=1
            union 
            SELECT distinct sec_id from [CD_10_SEC].[dbo].[FND_D_MKT_YIELD] with(nolock) WHERE is_vld = 1 
            and f0010 = '%s' and f0020 is not null
            """ % (date, date)
        else:
            """得到所有未退市的基金"""
            query = """
            select distinct (sec_id) from CD_10_SEC.DBO.FND_D_FACT  with(nolock) 
            where is_vld=1 and (del_dt is null or del_dt>getdate())
            """

        res = self.pb.read_sql(query)['sec_id'].tolist()

        return res


    def fetch_nav(self, sec_id_list = None, start = '19900101', end = None):
        """
        获取基金净值，返回DataFrame对象
        :param sec_id_list: 基金代码列表
        :param start: 开始日期（默认为19900101）
        :param end: 结束日期（默认为当前日期）
        :return: DataFrame对象
        """

        if end is None:
            end = self.end

        # 去除无效的净值
        query = """
        select f0010 as date,sec_id,F0060 as nav from CD_10_SEC.DBO.FND_D_NTVAL with(nolock)
        where not F0060 =0 and F0060 is not null and is_vld = 1 and f0010 between '%s' and '%s'
        """ % (start, end)
        # and sec_id in (%s)
        # """ % (start, end, ",".join(["'%s'" % sec_id for sec_id in sec_id_list]))
        # print(query)
        if sec_id_list:
            sec_id_str = " and sec_id in (" + ",".join(["'%s'" % sec_id for sec_id in sec_id_list]) + ")"
            query += sec_id_str

        res = self.pb.read_sql(query)

        return res

    def fetch_ret_mny(self, sec_id_list = None, start = '19900101', end = None):
        """
        获取货币型基金日收益，返回DataFrame对象
        :param sec_id_list: 基金代码列表
        :param start: 开始日期（默认为19900101）
        :param end: 结束日期（默认为当前日期）
        :return: DataFrame对象
        """

        if end is None:
            end = self.end

        # 去除无效的ret
        query = """
        SELECT a.f0010 as date, a.sec_id, a.f0020/10000 as ret from [CD_10_SEC].[dbo].[FND_D_MKT_YIELD] A with(nolock)
        INNER JOIN [CD_10_SEC].[dbo].[FND_D_TAG] B with(nolock) on a.sec_id=b.sec_id WHERE B.F1010=6 and 
        a.f0010 between '%s' and '%s' and a.is_vld=1 and b.is_vld=1 and a.f0020 is not null
        """ % (start, end)

        if sec_id_list:
            sec_id_str = " and a.sec_id in (" + ",".join(["'%s'" % sec_id for sec_id in sec_id_list]) + ")"
            query += sec_id_str

        res = self.pb.read_sql(query)

        return res

    def fetch_nt_val(self, start, end, sec_id_list = None):
        """
        获取已经入库的净值(注意：数据库保留四位小数 此处要保持一致)，返回DataFrame对象
        :param start: 开始日期
        :param end: 结束日期
        :param sec_id_list: 基金代码列表
        :return: DataFrame对象
        """

        sql = """
        select sec_id,pub_dt as date,nt_val from CD_10_IND.DBO.IND_S_FND_PEF_RET 
        where pub_dt >= '%s' and pub_dt <= '%s' and is_vld = 1
        """ % (start, end)

        if sec_id_list is not None:
            sec_id_str = " and sec_id in (" + ",".join(["'%s'" % sec_id for sec_id in sec_id_list]) + ")"
            sql = sql + sec_id_str

        nt_val_df = self.pb.read_sql(sql)

        if not nt_val_df.empty:
            nt_val_df['nt_val'] = nt_val_df['nt_val'].apply(lambda x: '%.4f' % x)

        return nt_val_df

    def fetch_index_fund_bench_ret(self, start = '19900101', end = None, is_filter_null = False):
        """
        得到指数基金的基准ret，返回DataFrame对象
        :param start: 开始日期（默认为19900101）
        :param end: 结束日期（默认为当前日期）
        :param is_filter_null: 是否过滤end当天未披露的基准RET的基金。日常更新置为True（默认为False）
        :return: DataFrame对象
        """

        if end is None:
            end = self.end

        if not is_filter_null:
            query = """
            select pub_dt as date, sec_id, chg_ratio as bench_ret
            from CD_10_IND.dbo.IND_S_FND_BENCH with(nolock)
            where stat_prd=30 and is_vld =1 and pub_dt between '%s' and '%s'
            """ % (start, end)
        else:
            # date 当天基准ret不为空的基金
            query = """
            select pub_dt as date, sec_id, chg_ratio as bench_ret
            from CD_10_IND.dbo.IND_S_FND_BENCH with(nolock)
            where stat_prd=30 and is_vld =1 and pub_dt between '%s' and '%s' and sec_id in 
            (select distinct sec_id from CD_10_IND.dbo.IND_S_FND_BENCH with(nolock) where pub_dt = '%s' and stat_prd = 30 
            and is_vld = 1 and chg_ratio is not null)
            """ % (start, end, end)

        res = self.pb.read_sql(query)

        return res

    def fetch_fund_category(self):
        """
        查询基金类型
        :return: DataFrame对象
        """

        query = """
            SELECT sec_id, f1020 'fnd_category', f2010 'inv_type' FROM CD_10_SEC.dbo.FND_D_TAG with(nolock) 
            where is_vld=1 and f1020 is not null
            """

        res = self.pb.read_sql(query)

        return res

    def fetch_bench_value(self):
        """
        得到最新的基准值
        :return: DataFrame对象
        """

        query = """
        select distinct pub_dt as date, lower(idx_cd) as id, F0050 as value 
        from CD_10_SEC.DBO.QOT_D_IDX with(nolock) 
        where idx_cd in ('H11008','H11006','000985') and pub_dt >= '19900101' and is_vld=1
        union
        select pub_dt as date, sec_id as id, chg_ratio as value
        from CD_10_IND.dbo.IND_S_FND_BENCH with(nolock)
        where stat_prd=30 and is_vld =1 and pub_dt >= '19900101'
        """

        res = self.pb.read_sql(query)

        return res


if __name__ == '__main__':
    # 测试
    pb = FundDataAccess()
    print(pb.fetch_fund_category())
    print(pb.check_trade_day('20200101'))
    # print(pb.fetch_calendar())
