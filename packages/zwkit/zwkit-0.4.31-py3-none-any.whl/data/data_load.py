import tushare as ts
##通过tushare API获取数据的函数
# 1、获取股票指数数据
# 2、根据指数的数据获取股票的数据
# 3、获取股票的日线数据
def get_index_data(token,index_code, start_date, end_date):
    """
    获取指数的数据
    :param index_code: 指数代码
    :param start_date: 开始日期
    :param end_date: 结束日期
    :return: 指数的数据
    """
    api = ts.pro_api(token)
    df = api.index_daily(ts_code=index_code, start_date=start_date, end_date=end_date)


    return df