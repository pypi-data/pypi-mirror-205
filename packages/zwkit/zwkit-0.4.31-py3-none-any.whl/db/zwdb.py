import clickhouse_driver
import clickhouse_kit as db

#获取股票日线的指定收益率
def get_stock_returns(conn: clickhouse_driver.dbapi.Connection, symbol_list:str, start_date: str, end_date: str, shift_num: int):
    """
    :param conn:
    :param symbol_list:
    :param start_date:
    :param end_date:
    :param shift_num:
    :return:
    """
    limit = shift_num * 2
    # 1 获取end_date的后shift_num * 2个交易日
    sql = "select trade_date from basic_stock_workday where trade_date>= '%s' order by trade_date limit %s" % (end_date, limit)
    workday_list = db.clickhouse_select(conn, sql)['trade_date']
    if len(workday_list) < limit:
        # 抛出异常
        raise Exception("交易日不足")
    new_end_date = str(workday_list.iloc[-1])
    # 2 获取日线数据 并以symbol和trade_date正序排序
    sql = "select symbol,trade_date,pct_chg from basic_stock_daily where symbol = '%s' and trade_date>='%s' and trade_date<='%s' order by symbol,trade_date" % (
        symbol_list, start_date, new_end_date)
    daily_data = db.clickhouse_select(conn, sql)
    daily_data['pct_chg'] = daily_data['pct_chg'].shift(-shift_num)
    daily_data['trade_date'] = daily_data['trade_date'].apply(lambda x: str(x))
    daily_data = daily_data[(daily_data['trade_date']>=start_date) & (daily_data['trade_date']<=end_date)]
    return daily_data