import akshare as ak
import pandas as pd

# 获取中证1000指数历史数据
stock_zh_index_daily_df = ak.stock_zh_index_daily(symbol="sh000852")
print(stock_zh_index_daily_df)

# 将日期列转换为datetime格式
stock_zh_index_daily_df['date'] = pd.to_datetime(stock_zh_index_daily_df['date'])

# 设置日期列为索引
stock_zh_index_daily_df.set_index('date', inplace=True)
# 使用fillna和ffill填充缺失值
stock_zh_index_daily_df_filled = stock_zh_index_daily_df.fillna(method='ffill')

print(stock_zh_index_daily_df_filled)

# 计算每年的涨幅
annual_return = stock_zh_index_daily_df_filled['close'].resample('Y').ffill().pct_change()


# 将年度涨幅结果格式化为百分比
annual_return = annual_return * 100
print(annual_return)
print(','.join(['{:.2f}'.format(x/100+1) for x in annual_return]))
