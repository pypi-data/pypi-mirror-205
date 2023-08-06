import clickhouse_driver
import pandas as pd


def create_conn(address: str, port: int, database: str, user: str, password: str = ""):
    """
    初始化连接
    :return:
    """
    conn = clickhouse_driver.connect(dsn=f'clickhouse://{user}:{password}@{address}:{port}/{database}?connect_timeout=3000000&send_receive_timeout=3000000'
                                         '&sync_request_timeout=3000000')
    return conn


def clickhouse_insert(df, table_name, conn: clickhouse_driver.connect):
    conn = conn
    cursor = conn.cursor()
    query = fill_sql(df, table_name)
    cursor.execute(query)
    conn.commit()
    cursor.close()


def clickhouse_select(conn: clickhouse_driver.connect, sql: str):
    conn = conn
    cursor = conn.cursor()
    cursor.execute(sql)
    result = cursor.fetchall()
    cursor.close()
    df = pd.DataFrame(result, columns=[i[0] for i in cursor.description])
    return df


def fill_sql(df, table_name):
    sql = f"INSERT INTO {table_name} VALUES "
    values = []
    for row in df.itertuples(index=False):
        row_values = []
        for value in row:
            if isinstance(value, str):
                row_values.append(f"'{value}'")
            else:
                row_values.append(str(value))
        values.append(f"({', '.join(row_values)})")
    sql += ', '.join(values)
    return sql
